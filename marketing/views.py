import csv

from django.http import StreamingHttpResponse
from django.http import HttpResponse
import json
import _mysql
db=_mysql.connect(host="127.0.0.1",user="useradvdb",
                  passwd="tydHQDP^^###!!18100108",db="adv")





class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def get_file(campaign, location,age, gender, limit):

    db.query("SELECT id, sdt, facebook from mkt where {} and {} and {} and{} limit {}".
             format(campaign, location, age, gender, limit))
    r = db.store_result()
    rows = r.fetch_row(0)

    # cursor.close()
    return list(rows)



def add_condition(condition, value):
    if value !="":
        value = value.replace("-",",")
        result = condition + " in ({})".format(value)
    else:
        result = "1=1"
    return result

def get_mkt_file(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.


    campaign = request.GET.get("campaign","")
    campaign = add_condition("campaign",campaign)
    location = request.GET.get("location","")
    location = add_condition("location",location)

    age = request.GET.get("age","")
    age = add_condition("age",age)

    gender = request.GET.get("gender","")
    gender = add_condition("gender", gender)

    limit = request.GET.get("limit","")


    rows = get_file(campaign, location,age, gender, limit)

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="hehe.csv"'


    # response = HttpResponse(json.dumps("abc"))

    # cursor.close()
    # cnx.close()

    return response




def test(request):

    return HttpResponse(json.dumps("hello"))