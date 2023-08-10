const pointMap = {
  '博学': point1,
  '校七': point2,
  '校四': point3,
  '华侨': point4,
  '博远': point5,
  '慎思': point6,
  '诚明': point7,
  '明辨': point8,
  '校六': point9,
  '体育馆': point10,
  '校五': point11,
  '博纳': point13,
  '校二': point14,
  '西门': point16,
  '琢玉讲堂': point18,
  '三食堂': point19,
  '南门': point20,
  '北门': point21,
  '乒羽馆': point22,
  '青春广场': point23,
  '行知楼': point24,
  '二食堂': point25,
  '澡堂': point27,
  '赛欧': point28,
  '经贸广场': point29
};

// 获取起始点和终点地名
const startLocation = selectA.value;
const endLocation = selectB.value;

// 根据地名获取对应的坐标点
const startPoint = pointMap[startLocation];
const endPoint = pointMap[endLocation];

// 使用起始点和终点的坐标点进行后续操作
console.log('起始点坐标：', startPoint);
console.log('终点坐标：', endPoint);

// 获取起始点和终点的坐标
var start = new BMapGL.Point(startPoint.lng, startPoint.lat);
var end = new BMapGL.Point(endPoint.lng, endPoint.lat);
var way1 = new BMapGL.Point(startPoint.lng, startPoint.lat);;
var way2 = new BMapGL.Point(endPoint.lng, endPoint.lat);
var startMarker = new BMapGL.Marker(start);
var endMarker = new BMapGL.Marker(end);
var way1Marker = new BMapGL.Marker(way1);
var way2Marker = new BMapGL.Marker(way2);

map.addOverlay(startMarker);
map.addOverlay(endMarker);
map.addOverlay(way1Marker);
map.addOverlay(way2Marker);