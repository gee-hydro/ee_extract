pkgs.agg_Tair = function (col, band) {
  band = band || "Tair";
  col = col.select(band);

  var Tmin = col.min();
  var Tmax = col.max();
  var Tavg = col.mean();
  return ee.Image([Tmin, Tmax, Tavg]).rename(["Tmin", "Tmax", "Tavg"]);
}

pkgs.aggregate = function (imgcol, prop, reducer) {
  var props = ee.Dictionary(imgcol.aggregate_histogram(prop)).keys();//.getInfo();
  var col_tmp = props.map(function (p) {
    return ee.Image.constant(0).set('dn', p);
  });

  var res = ee.Join.saveAll('matches', 'measure')
    .apply(col_tmp, imgcol, ee.Filter.equals({ leftField: prop, rightField: prop }))
    .toList(col_tmp.size())
    .map(function (img) {
      img = ee.Image(img);
      var r = ee.ImageCollection.fromImages(img.get('matches'));
      var ans = r.reduce(reducer);
      var _prop = img.get(prop);
      var date = prop == "dn" ? pkgs.YearDn2date(_prop, 8) : img.date();
      var id = date.format('yyyy_MM_dd');
      return ee.Image(ans)
        .set(prop, _prop)
        .set('system:id', id)
        .set('system:index', id)
        .set('system:time_start', date.millis());
    });
  res = ee.ImageCollection(res);
  var bands_old = imgcol.first().bandNames();
  var bands_new = res.first().bandNames();
  return res.select(bands_new, bands_old);
};
