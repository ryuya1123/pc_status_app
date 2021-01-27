import sys                                                                                                                                     
import re
import subprocess
import dateutil.parser

def attendanceDate(month):
    output = {}
    checkMonth = [0]
    def assignDate(matchDate, func):
        parseDate = dateutil.parser.parse(matchDate)
        if checkMonth[0]:
            if checkMonth[0] is not parseDate.month: return

        if parseDate.month is month:
            dateStr = parseDate.day
            if dateStr in output:
                if job in output[dateStr]:
                    output[dateStr][job] = parseDate if func(output[dateStr][job], parseDate) else output[dateStr][job]
                else:
                    output[dateStr].update({job: parseDate})
            else:
                output[dateStr] = {job: parseDate}
            checkMonth[0] = parseDate.month

    for job, func in {'reboot': lambda x,z:x>z, 'shutdown': lambda x,z:x<z}.items():
        for checkDate in subprocess.check_output("last %s" % job, shell=True).splitlines():
            matchObj = re.findall(r'%s\s+\~\s+([a-zA-Z]{3}\s[a-zA-Z]{3}\s+\d{1,2}\s+\d{1,2}\:\d{1,2})\s' % job, checkDate.decode('utf-8'))
            if len(matchObj): assignDate(matchObj[0], func)

    return output

def value():
    for key, value in sorted(attendanceDate(int(sys.argv[1])).items(), key=lambda x: x[0]):
        return print('%s/%s %s, %s' % (int(sys.argv[1]), key,
                        'start %s' % value['reboot'].strftime('%H:%M') if 'reboot' in value else '',
                        'end %s' % value['shutdown'].strftime('%H:%M') if 'shutdown' in value else ''))

value()
