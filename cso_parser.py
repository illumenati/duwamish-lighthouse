import csv
import logging
import logging.handlers
import threading
import time
import traceback
import requests


formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')

logger = logging.getLogger('cso_parser')
logger.setLevel(logging.INFO)
logger.propagate = 0

file_handler = logging.handlers.RotatingFileHandler('cso_log.log', maxBytes=10 * 1024 * 1024, backupCount=2)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


class CsoParser:
    """
    This class runs a thread that gathers Combined Sewer Overflow (CSO) data periodically. It gathers the data from
    http://your.kingcounty.gov/dnrp/library/wastewater/cso/img/cso.csv, then parses the CSV, and returns a formatted
    version of the data.
    """

    csv_url = 'http://your.kingcounty.gov/dnrp/library/wastewater/cso/img/cso.csv'

    def __init__(self, requested=None):
        # requested is a set of CSO TagName strings 
        self.requested = requested
        self.now_count = 0
        self.recent_count = 0
        self.not_count = 0
        self.not_real_time_count = 0

    def _get_csv(self):
        logger.info('Retrieving CSV file.')

        # Stream the CSV so we don't eat a bunch of RAM.
        r = requests.get(self.csv_url, stream=True)
        with open('cso.csv', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()

    def _parse_csv(self):
        """
        CSV Format: [cso identifier],[status code]

        The City CSOs are labeled with their NPDES number while the County CSOs are labeled by name.

        The status code indicates:
        1 = CSO discharging now
        2 = CSO discharged in last 48 hrs
        3 = CSO not discharging
        4 = Real time data not available
        """
        logger.info('Parsing CSV file')
        reader = csv.reader(open('cso.csv', 'r'))
        first_line = True
        now_count = 0
        recent_count = 0
        not_count = 0
        not_real_time_count = 0
        row_count = 0

        for row in reader:
            if not first_line:
                row_count += 1
                cso, status = row
                
                # default to tracking all CSOs
                if self.requested is not None and cso in self.requested:
                    if status == '1':
                        now_count += 1
                    elif status == '2':
                        recent_count += 1
                    elif status == '3':
                        not_count += 1
                    elif status == '4':
                        not_real_time_count += 1
            else:
                first_line = False

        self.now_count = now_count
        self.recent_count = recent_count
        self.not_count = not_count
        self.not_real_time_count = not_real_time_count
        self.last_update = time.time()

        log_msg = 'Rows: {}, Now Count: {}, Recent Count: {}, No Count: {}, Not Real Time: {}'
        logger.info(log_msg.format(row_count, now_count, recent_count, not_count, not_real_time_count))

    def update(self):
        try:
            self._get_csv()
        except Exception:
            logger.exception('Error retrieving CSV!')
            traceback.print_exc()
        else:
            # Only parse the csv if we successfully retrieve it.
            try:
                self._parse_csv()
            except Exception:
                logger.exception('Error parsing CSV!')
                traceback.print_exc()

if __name__ == '__main__':
    r = {"KDOM.CSOSTATUS_N", "HARB.CSOSTATUS_N", "CHEL.CSOSTATUS_N", "LAND.CSOSTATUS_N", "HANF.CSOSTATUS_N",
                 "DUWA.CSOSTATUS_N", "BRAN.CSOSTATUS_N", "T115.CSOSTATUS_N", "MICH.CSOSTATUS_N", "WMIC.CSOSTATUS_N",
                 "EMAR.CSOSTATUS_N", "8TH.CSOSTATUS_N", "NORF.CSOSTATUS_N", "NPDES078", "NPDES080", "NPDES107",
                 "NPDES116"}
    c = CsoParser(r)
    c.csv_url = 'http://localhost:8080/'
    c.update()
    print(c.now_count, c.recent_count, c.not_count, c.not_real_time_count)
