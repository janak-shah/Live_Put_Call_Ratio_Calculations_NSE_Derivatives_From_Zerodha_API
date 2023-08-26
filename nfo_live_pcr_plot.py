import mysql
import mysql.connector
import datetime
from bokeh.io import output_notebook, show,save
from bokeh.plotting import figure, output_file, save
# from bokeh.layouts import gridplot
from bokeh.layouts import column
import time
from bokeh.models import PanTool, ResetTool, HoverTool
from bokeh.models import ColumnDataSource

con1 = mysql.connector.connect(
  host="144.217.75.173",
  user="tmrlive_junky7",
  passwd="Met2davos",
  database = "tmrlive_tmralgo"
)



db = con1.cursor()
print("TMR ALGO DB CONNECTED")


def data_retrieve(stockname):

    datey = []
    calls = []
    puts = []
    pcr = []
    spot = []
    
    db.execute("SELECT * FROM {} ORDER BY time".format(stockname+"livepcr"))
    
    for row in db.fetchall():
        # k = datetime.date(row[0])
        datey.append(row[0])
        calls.append(row[3])
        puts.append(row[2])
        pcr.append(row[4])
        spot.append(row[5])
    
    print(datey)
# =============================================================================
#     print(calls)
#     print(puts)
    print(pcr)
#     print(spot)
#     n = len(calls)
# =============================================================================
    data1= {'dates':datey,
           'spot': spot,
           'calls': calls,
           'puts': puts,
           'pcr': pcr}


    source1 = ColumnDataSource(data = data1)
    print(source1)
    
    
    
    
    s = figure(x_axis_type="datetime",plot_width=1200, plot_height=400, title="{}".format(stockname)+"Spot"+"{}".format(datey[-1]))
    s.line(x='dates',y='spot', line_width=2, source=source1, color = 'darkorange')
    s.xaxis.axis_label = "SPOT"
    hover = HoverTool(tooltips = [("Date",'@dates{%F,%H:%M}'),("Price",'@spot{%0.2f}')],formatters = {'dates':'datetime','spot':'printf'})
    hover.mode = "mouse"
    s.add_tools(hover)
    s.toolbar.logo = None
    # =============================================================================
    # show(p) # show the results
    # =============================================================================
    p = figure(x_axis_type="datetime",plot_width=1200, plot_height=400, title="{}".format(stockname)+"PCR"+"{}".format(datey[-1]))
    #p.line(datey,pcr, line_width=2, color = "teal")
    p.xaxis.axis_label = "PCR"
    p.line(x='dates',y='pcr', line_width=2, source=source1,color = "purple")
    
    hover = HoverTool(tooltips = [("Date",'@dates{%F,%H:%M}'),("PCR",'@pcr{%0.2f}')], formatters = {'dates':'datetime','pcr':'printf'})
    hover.mode = "mouse"
    p.add_tools(hover)
    p.toolbar.logo = None
    # =============================================================================
    # show(p) # show the results
    # =============================================================================
    q = figure(x_axis_type="datetime",plot_width=1200, plot_height=400, title = "Total Calls")
    #q.line(datey, calls, line_width=2, color = "aquamarine")
    q.xaxis.axis_label = "Total Calls"
    q.line(x='dates',y='calls', line_width=2, source=source1,color = "hotpink")
    
    hover = HoverTool(tooltips = [("Date",'@dates{%F,%H:%M}'),("Calls",'@calls{%0.2f}')], formatters = {'dates':'datetime','calls':'printf'})
    
    hover.mode = "mouse"
    q.add_tools(hover)
    q.toolbar.logo = None
    # =============================================================================
    # show(q) # show the results
    # =============================================================================
    r = figure(x_axis_type="datetime",plot_width=1200, plot_height=400, title = "Total Puts")
    #r.line(datey, puts, line_width=2, color = "hotpink")
    r.xaxis.axis_label = "Total Puts"
    r.line(x='dates',y='puts', line_width=2, source=source1, color = "aquamarine")
    hover = HoverTool(tooltips = [("Date",'@dates{%F,%H:%M}'),("Puts",'@puts{%0.2f}')], formatters = {'dates':'datetime','puts':'printf'})
    
    hover.mode = "mouse"
    r.add_tools(hover)
    r.toolbar.logo = None

    s = column(s,p,q,r)
# =============================================================================
    filename = "{}.html".format(stockname+"livepcr")
    output_file(filename)
    return(s)

stockname = input("Enter a Stockname").upper()

print(stockname)
y = data_retrieve(stockname)
show(y)

while True:
    print("STARTING NOW ")
    print(datetime.datetime.now())
    time.sleep(30)
    y = data_retrieve(stockname)
    save(y)
    




