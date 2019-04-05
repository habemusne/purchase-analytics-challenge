import csv
import logging
from sys import argv
from os.path import exists, isdir
from collections import defaultdict, namedtuple

# Global variables specifying the format of the input and output csvs
ROW_TYPES_ORDER_PROD_CSV = [int, int, int, int]
ROW_TYPES_PROD_CSV = [int, str, int, int]
HEADER_REPORT_CSV = ['department_id', 'number_of_orders', 'number_of_first_orders', 'percentage']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


def _iter_read_csv(csv_path, row_types):
    """
    Iterate over a csv and yield every row unless it's expected.

    Args:
        path_prod: path to the product csv (including file name)
        path_order_prod: path to the order-product csv (including file name)
    """

    with open(csv_path, 'r') as f:
        # Read over the csv
        reader = csv.reader(f)
        reader.__next__()
        for i, row in enumerate(reader):
            # Skip the row if it has unexpected row length
            if len(row) != len(row_types):
                logger.warning('Unexpected row length at row {}'.format(i))
                continue

            # skip the row if it has unexpected data types
            good_format = True
            row = [cell.strip() for cell in row]  # avoid whitespaces
            for j, cell in enumerate(row):
                #TODO other data types (bool, float, etc) need further support
                if row_types[j] not in [int, str]:
                    raise NotImplementedError('cleaning data type {} is not implemented: row {}'.\
                        format(row_types[j].__name__, i))

                # if cell needs to be string, go ahead. if needs to be int, check if it's number
                good_format &= (row_types[j] == str) or (row_types[j] == int and cell.isdigit())

            if not good_format:
                logger.warning('Unexpected row format at row {}'.format(i))
                continue

            row = [row_types[j](cell) for j, cell in enumerate(row)]
            yield row


def analyze(path_order_prod, path_prod, path_report):
    """
    Perform analytics for the challenge task.

    Args:
        path_order_prod: path to the order-product csv (including file name)
        path_prod: path to the product csv (including file name)
        path_report: path to the output report csv (including file name)

    Raise:
        FileNotFoundError: if <csv_path> does not exist as a file or
            there is no directory for report csv to reside.
    """

    # Check file and dir existence
    for path in [path_order_prod, path_prod]:
        if not exists(path):
            raise FileNotFoundError(path)
    out_dir = '/'.join(path_report.split('/')[:-1])
    if not isdir(out_dir):
        raise FileNotFoundError(out_dir)

    # Build a mapping from product id to department id
    logger.info('Generating data from {}...'.format(path_prod.split('/')[-1]))
    prodid_to_deptid = {}
    iterator = _iter_read_csv(path_prod, ROW_TYPES_PROD_CSV)
    for row in iterator:
        prodid_to_deptid[row[0]] = row[3]

    # Read over order-product csv to count necessary statistics
    logger.info('Generating data from {}...'.format(path_order_prod.split('/')[-1]))
    deptid_stat = defaultdict(lambda: [0, 0])
    iterator = _iter_read_csv(path_order_prod, ROW_TYPES_ORDER_PROD_CSV)
    for i, row in enumerate(iterator):
        # if reordered flag is not 0 or 1, skip
        if row[3] not in [0, 1]:
            logger.warning('Unexpected reordered flag at row {} of {}.'.format(i, path_order_prod))
            continue

        # if product id is not in product csv, skip
        if row[1] not in prodid_to_deptid:
            logger.warning('Product id not found in product csv: {}'.format(row[1]))
            continue
    
        deptid_stat[prodid_to_deptid[row[1]]][0] += 1
        deptid_stat[prodid_to_deptid[row[1]]][1] += int(not row[3])

    # Use the statistics to generate the report csv
    logger.info('Generating report...')
    with open(path_report, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER_REPORT_CSV)
        for deptid, stat in sorted(deptid_stat.items()):  # sort to keep departments in order
            writer.writerow([deptid, stat[0], stat[1], '%.2f' % (stat[1] / stat[0])])


if __name__ == '__main__':
    # Check each required mode and run it if necessary
    if len(argv) != 4:
        msg = 'Wrong number of arguments. Make sure you use python3 purchase_analytics.py' +\
            ' <path to order product csv> <path to product csv> <path to report csv>'
        logger.error(msg)
        exit(1)
    logger.info('Analyzig data...')
    try:
        analyze(*argv[1:])
    except FileNotFoundError as e:
        logger.error('File not found: ' + str(e))
        exit(1)
    logger.info('Done.')
