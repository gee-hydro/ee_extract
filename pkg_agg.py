import ee
from ee_PML import *

def seq_date(date_begin, date_end, by=1):
  day_secs = 86400000
  by = by * day_secs
  return ee.List.sequence(date_begin.millis(), date_end.millis(), by) \
      .map(ee.Date)


def date_format(date):
  return date.format("yyyy_MM_dd")


def agg_Tair(col, band="Tair"):
  col = col.select(band)
  Tmin = col.min()
  Tmax = col.max()
  Tavg = col.mean()
  return ee.Image.cat([Tmin, Tmax, Tavg]).rename(["Tmin", "Tmax", "Tavg"])


def agg_daily(date_beg, col, bands_mean):
  date_beg = ee.Date(date_beg)
  date_end = date_beg.advance(1, 'day')
  _col = col.filterDate(date_beg, date_end)

  # 'bands_mean' should be defined elsewhere in your code
  img = _col.select(bands_mean).mean()
  # 'pkgs.agg_Tair' needs to be defined as per your existing code
  img_Tair = agg_Tair(_col, "Tair")
  img = img.addBands(img_Tair) \
      .set('system:id', date_format(date_beg)) \
      .set('system:index', date_format(date_beg)) \
      .set('system:time_start', date_beg.millis())
  return img


def aggregate(imgcol, prop, reducer):
  props = ee.Dictionary(imgcol.aggregate_histogram(prop)).keys()
  col_tmp = props.map(lambda p: ee.Image.constant(0).set('dn', p))

  def process_image(img):
    img = ee.Image(img)
    r = ee.ImageCollection.fromImages(img.get('matches'))
    ans = r.reduce(reducer)
    _prop = img.get(prop)
    date = ee.Date(pkgs.YearDn2date(_prop, 8)
                   ) if prop == "dn" else img.date()
    id = date.format('yyyy_MM_dd')
    return ee.Image(ans) \
        .set(prop, _prop) \
        .set('system:id', id) \
        .set('system:index', id) \
        .set('system:time_start', date.millis())

  res = ee.Join.saveAll('matches', 'measure') \
      .apply(col_tmp, imgcol, ee.Filter.equals(leftField=prop, rightField=prop)) \
      .toList(col_tmp.size()) \
      .map(process_image)
  res = ee.ImageCollection(res)
  bands_old = imgcol.first().bandNames()
  bands_new = res.first().bandNames()
  return res.select(bands_new, bands_old)


def get_daily_GLDAS(year_beg, year_end, bands_mean):
  def process(date_beg):
    return agg_daily(date_beg, col_gldas, bands_mean)

  col_gldas = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H")\
      .select(list(bands_GLDAS21.values()), list(bands_GLDAS21.keys())) \
      .filter(ee.Filter.calendarRange(year_beg, year_end, "year"))
    #   .filterDate(date_beg, date_end)
  date_beg = ee.Date(f"{year_beg}-01-01")
  date_end = ee.Date(f"{year_end}-12-31")
  dates = seq_date(date_beg, date_end)
  res = dates.map(process)
  res = ee.ImageCollection(res)
  return res
