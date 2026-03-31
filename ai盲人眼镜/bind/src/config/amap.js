// 高德地图API配置
// 请替换为您自己的高德地图API密钥
// 获取API密钥的步骤：
// 1. 访问 https://console.amap.com/dev/key/app
// 2. 注册/登录高德开放平台账号
// 3. 创建应用并获取API密钥
// 4. 在应用设置中添加Web服务

export const AMAP_CONFIG = {
    // 高德地图API密钥
    key: '1056fa849b373f55dc6f615aeeb54b11',

    // 安全密钥
    securityCode: 'fff4bed2bdddd2bfbac74469f6220579',

    // 地图默认配置
    defaultCenter: [116.4074, 39.9042], // 默认中心点（北京天安门）
    defaultZoom: 17, // 默认缩放级别

    // 3D配置
    viewMode: '3D', // 2D或3D视图
    pitch: 50, // 地图俯视角度（0-83）
    rotation: 0, // 地图旋转角度

    // 地图样式
    mapStyle: 'amap://styles/normal', // 地图样式
    skyColor: '#1E3A8A', // 天空颜色

    // 功能开关
    showBuildingBlock: true, // 显示建筑物
    buildingAnimation: true, // 建筑物动画
    showLabel: true, // 显示文字标记

    // 缩放级别范围
    zooms: [3, 20]
}

// 获取当前位置（使用浏览器定位API）
export const getCurrentPosition = () => {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('浏览器不支持定位功能'))
            return
        }

        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    longitude: position.coords.longitude,
                    latitude: position.coords.latitude
                })
            },
            (error) => {
                reject(error)
            }, {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 60000
            }
        )
    })
}