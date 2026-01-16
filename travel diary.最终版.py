#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旅游日记网页生成器（支持直接上传图片，无需本地文件）
核心升级：图片上传功能（Base64存储）
"""

import datetime
import os
import json
import platform  # 用于跨系统获取桌面路径

def generate_travel_diary():
    desktop_path = r"D:\用户\Lenovo\Desktop\Travel Diary"
    # 打印路径，方便排查
    print(f"📌 目标生成路径：{desktop_path}")
    generate_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 默认地点数据（初始图片为空，后续通过上传添加）
    default_visited_places = [
        {
            "name": "大理", 
            "lat": 25.6002, 
            "lng": 100.2489,
            "photos": ["https://github.com/traveldiary3/traveldiary3.github.io/raw/main/大理-1.jpg",
                       "https://github.com/traveldiary3/traveldiary3.github.io/raw/main/大理-2.jpg",
                       "https://github.com/traveldiary3/traveldiary3.github.io/raw/main/大理-3.jpg",
                       "https://github.com/traveldiary3/traveldiary3.github.io/raw/main/大理-4.jpg"],  
            "desc": ""
        },
        {
            "name": "弥勒", 
            "lat": 24.4117, 
            "lng": 103.4148,
            "photos": ["https://github.com/traveldiary3/traveldiary3.github.io/raw/main/弥勒-1.jpg",
                       "https://github.com/traveldiary3/traveldiary3.github.io/raw/main/弥勒-2.jpg",
                       "https://github.com/traveldiary3/traveldiary3.github.io/raw/main/弥勒-3.jpg",
                       "https://github.com/traveldiary3/traveldiary3.github.io/raw/main/弥勒-5.jpg"],
            "desc": ""
        },
        {
            "name": "贵阳", 
            "lat": 26.5783, 
            "lng": 106.7134,
            "photos": ["https://github.com/traveldiary3/traveldiary3.github.io/raw/main/贵阳-1.jpg",
                       "https://github.com/traveldiary3/traveldiary3.github.io/raw/main/贵阳-2.jpg",
                       "https://github.com/traveldiary3/traveldiary3.github.io/raw/main/贵阳-3.jpg",
                       "https://github.com/traveldiary3/traveldiary3.github.io/raw/main/贵阳-4.jpg",
                       "https://github.com/traveldiary3/traveldiary3.github.io/raw/main/贵阳-5.jpg"],
            "desc": ""
        },
        {
            "name": "南宁", 
            "lat": 22.8177, 
            "lng": 108.3663,
            "photos": ["https://github.com/traveldiary3/traveldiary3.github.io/raw/main/南宁-1.jpg"],
            "desc": ""
        },
        {
            "name": "楚雄", 
            "lat": 25.0329, 
            "lng": 101.5461,
            "photos": ["https://github.com/traveldiary3/traveldiary3.github.io/raw/main/楚雄-1.jpg",
                       "https://github.com/traveldiary3/traveldiary3.github.io/raw/main/楚雄-2.jpg"],
        }
    ]
    default_want_to_go_places = [
        {"name": "云南丽江", "lat": 26.8641, "lng": 100.2363},
        {"name": "新疆伊犁", "lat": 43.9208, "lng": 81.3378},
        {"name": "西藏拉萨", "lat": 29.6546, "lng": 91.1250}
    ]

    default_visited_json = json.dumps(default_visited_places, ensure_ascii=False)
    default_want_json = json.dumps(default_want_to_go_places, ensure_ascii=False)

    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我们的旅游日记</title>
    <style>
        /* 全局样式 */
        body {{
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .container {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .btn {{
            padding: 10px 20px;
            margin: 10px 5px;
            border: none;
            border-radius: 4px;
            background-color: #3498db;
            color: white;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }}
        .btn:hover {{
            background-color: #2980b9;
        }}
        .function-area {{
            margin: 15px 0;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            display: none;
        }}
        .visited-place {{
            margin: 8px 0;
            color: #2980b9;
            cursor: pointer;
            text-decoration: underline;
        }}
        .visited-place:hover {{
            color: #1a5276;
        }}
        /* 照片展示区域 */
        .photo-container {{
            margin: 10px 0;
            padding: 20px;
            border: 1px solid #eee;
            border-radius: 4px;
            display: none;
            text-align: center;
        }}
        .photo-container img {{
            max-width: 100%;
            max-height: 500px;
            border-radius: 8px;
            margin: 10px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .photo-nav {{
            margin: 10px 0;
        }}
        .photo-nav button {{
            padding: 8px 16px;
            margin: 0 5px;
            border: 1px solid #3498db;
            background-color: white;
            color: #3498db;
            border-radius: 4px;
            cursor: pointer;
        }}
        .photo-nav button:hover {{
            background-color: #3498db;
            color: white;
        }}
        .photo-index {{
            margin: 0 10px;
            color: #666;
        }}
        /* 地图样式 */
        #footprintMap {{
            width: 100%;
            height: 500px;
            border-radius: 4px;
            margin-top: 10px;
        }}
        .info-window {{
            padding: 10px;
            font-size: 14px;
        }}
        .info-window h5 {{
            margin: 0 0 5px 0;
            color: #2c3e50;
        }}
        /* 添加地点区域 */
        .add-area {{
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: #fff;
        }}
        .add-area h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        .form-group {{
            margin: 10px 0;
        }}
        .form-group label {{
            display: inline-block;
            width: 100px;
            font-weight: 500;
        }}
        .form-group input, .form-group textarea {{
            padding: 8px;
            width: 300px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .form-group textarea {{
            width: 80%;
            height: 100px;
            resize: vertical;
        }}
        /* 图片上传样式 */
        .photo-upload {{
            margin: 10px 0;
            padding: 10px;
            border: 2px dashed #ddd;
            border-radius: 4px;
            text-align: center;
            cursor: pointer;
            transition: border-color 0.3s;
        }}
        .photo-upload:hover {{
            border-color: #3498db;
        }}
        .photo-upload input {{
            display: none; /* 隐藏原生文件选择框 */
        }}
        .upload-tip {{
            color: #666;
            font-size: 12px;
            margin-top: 5px;
        }}
        /* 已上传图片预览 */
        .uploaded-preview {{
            margin: 10px 0;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .preview-item {{
            width: 100px;
            height: 100px;
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }}
        .preview-item img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .preview-item .delete-btn {{
            position: absolute;
            top: 5px;
            right: 5px;
            background-color: rgba(255,0,0,0.8);
            color: white;
            border: none;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            font-size: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .submit-btn {{
            padding: 8px 20px;
            background-color: #27ae60;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        }}
        .submit-btn:hover {{
            background-color: #219653;
        }}
        .want-to-go-item {{
            margin: 8px 0;
            color: #8e44ad;
        }}
        /* 地点介绍编辑区域 */
        .desc-edit-area {{
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: #fff;
        }}
        .desc-item {{
            margin: 15px 0;
            padding: 10px;
            border-bottom: 1px dashed #eee;
        }}
        .desc-item h4 {{
            margin: 0 0 8px 0;
            color: #2c3e50;
        }}
        .save-desc-btn {{
            background-color: #f39c12;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 10px;
        }}
        .save-desc-btn:hover {{
            background-color: #e67e22;
        }}
        .desc-display {{
            margin: 10px 0;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 4px;
            line-height: 1.8;
        }}
        /* 数据管理按钮 */
        .data-manage {{
            margin: 10px 0;
            padding: 10px;
            background-color: #f0f8ff;
            border-radius: 4px;
        }}
        .data-btn {{
            padding: 6px 12px;
            margin: 0 5px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            background-color: #9b59b6;
            color: white;
        }}
        .data-btn:hover {{
            background-color: #8e44ad;
        }}
    </style>
    <script type="text/javascript" src="https://webapi.amap.com/maps?v=1.4.15&key=4e4b5d200e52321234567890abcdefgh"></script>
</head>
<body>
    <div class="container">
        <h1>我们的旅游日记</h1>
        <p>这是我们小组的「旅行记忆收纳盒」—— 用 Python 串起每一段出发与停留的痕迹。在这里，你能摸到我们踩过的青石板温度，
        也能接住那些还没启程的向往；每一个地名背后，都是一段裹着风、沾着烟火的生活碎片，是我们把日子过成诗的小证据～</p>
        
        <!-- 数据管理按钮 -->
        <div class="data-manage">
            <button class="data-btn" onclick="clearAllData()">清空所有保存的数据</button>
            <button class="data-btn" onclick="resetToDefault()">恢复默认数据</button>
            <span style="color: #666; margin-left: 10px;">💡 所有内容自动保存，图片支持直接上传</span>
        </div>
        
        <!-- 地点介绍编辑区域 -->
        <div class="desc-edit-area">
            <h3>✏️ 编辑地点介绍</h3>
            <div id="descEditContainer">
                <!-- 动态生成编辑框 -->
            </div>
        </div>
        
        <!-- 地点介绍展示区域 -->
        <div id="descDisplayArea">
            <!-- 动态展示介绍 -->
        </div>

        <!-- 添加旅行地点区域 -->
        <div class="add-area">
            <h3>添加旅行地点</h3>
            <!-- 添加去过的地方（支持图片上传） -->
            <div>
                <h4>✅ 添加去过的地方</h4>
                <div class="form-group">
                    <label>地名：</label>
                    <input type="text" id="addVisitedName" placeholder="例如：昆明" required>
                </div>
                <div class="form-group">
                    <label>纬度：</label>
                    <input type="number" step="0.0001" id="addVisitedLat" placeholder="例如：25.0479" required>
                </div>
                <div class="form-group">
                    <label>经度：</label>
                    <input type="number" step="0.0001" id="addVisitedLng" placeholder="例如：102.7126" required>
                </div>
                <!-- 图片上传区域 -->
                <div class="form-group">
                    <label>图片：</label>
                    <div class="photo-upload" onclick="document.getElementById('photoFile').click()">
                        <span>点击上传图片（支持多张）</span>
                        <input type="file" id="photoFile" accept="image/*" multiple onchange="handlePhotoUpload(this)">
                    </div>
                    <div class="upload-tip">支持JPG/PNG格式，每张图片不超过5MB</div>
                    <!-- 已上传图片预览 -->
                    <div class="uploaded-preview" id="uploadedPreview">
                        <!-- 动态生成预览图 -->
                    </div>
                </div>
                <div class="form-group">
                    <label>介绍：</label>
                    <textarea id="addVisitedDesc" placeholder="输入这个地点的介绍文字"></textarea>
                </div>
                <button class="submit-btn" onclick="addVisitedPlace()">添加</button>
            </div>
            
            <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">
            
            <!-- 添加想去的地方 -->
            <div>
                <h4>🔵 添加想去的地方</h4>
                <div class="form-group">
                    <label>地名：</label>
                    <input type="text" id="addWantName" placeholder="例如：香格里拉" required>
                </div>
                <div class="form-group">
                    <label>纬度：</label>
                    <input type="number" step="0.0001" id="addWantLat" placeholder="例如：27.8974" required>
                </div>
                <div class="form-group">
                    <label>经度：</label>
                    <input type="number" step="0.0001" id="addWantLng" placeholder="例如：99.7462" required>
                </div>
                <button class="submit-btn" onclick="addWantToGoPlace()">添加</button>
            </div>
        </div>

        <button class="btn" id="visitedBtn">我们去过的地方</button>
        <button class="btn" id="wantToGoBtn">我们想去的地方</button>
        <button class="btn" id="footprintBtn">我的足迹图</button>
        
        <!-- 已打卡地点列表 -->
        <div class="function-area" id="visitedList">
            <h3>已打卡的地点：</h3>
            <div id="visitedListContent">
                <!-- 动态生成列表 -->
            </div>
            <!-- 照片展示区域 -->
            <div class="photo-container" id="photoBox">
                <h4 id="photoTitle">旅游照片</h4>
                <img id="currentPhoto" src="" alt="旅游照片">
                <div class="photo-nav">
                    <button id="prevBtn">上一张</button>
                    <span class="photo-index" id="photoIndex">1/1</span>
                    <button id="nextBtn">下一张</button>
                </div>
            </div>
        </div>
        
        <!-- 想去的地方列表 -->
        <div class="function-area" id="wantToGoList">
            <h3>计划打卡的地点：</h3>
            <div id="wantToGoListContent">
                <!-- 动态生成列表 -->
            </div>
        </div>
        
        <!-- 足迹地图 -->
        <div class="function-area" id="footprintArea">
            <h3>我的旅游足迹图</h3>
            <p>🔴 红色标记：已打卡的城市 | 🔵 蓝色标记：计划打卡的城市</p>
            <p>点击标记可查看城市名称和介绍</p>
            <div id="footprintMap"></div>
        </div>
    </div>

    <script>
        /* 全局变量 */
        let map = null;
        let visitedPoints = [];  // 存储去过的地方（含Base64图片）
        let wantToGoPoints = [];
        let mapMarkers = [];
        
        let currentCityPhotos = [];  // 当前城市的Base64图片列表
        let currentPhotoIndex = 0;
        let uploadedPhotos = [];     // 临时存储待添加地点的上传图片（Base64）

        // 本地存储KEY
        const STORAGE_KEY_VISITED = 'travel_diary_visited';
        const STORAGE_KEY_WANT = 'travel_diary_want';
        // 默认数据
        const DEFAULT_VISITED = {default_visited_json};
        const DEFAULT_WANT = {default_want_json};

        // ========== 核心：图片上传与Base64转换 ==========
        /**
         * 处理图片上传：将图片转为Base64格式，并显示预览
         */
        function handlePhotoUpload(fileInput) {{
            const files = fileInput.files;
            if (!files.length) return;

            // 遍历选择的文件
            for (let i = 0; i < files.length; i++) {{
                const file = files[i];
                // 验证文件类型和大小
                if (!file.type.startsWith('image/')) {{
                    alert('请选择图片文件！');
                    continue;
                }}
                if (file.size > 5 * 1024 * 1024) {{ // 5MB限制
                    alert('图片大小不能超过5MB！');
                    continue;
                }}

                // 使用FileReader将图片转为Base64
                const reader = new FileReader();
                reader.onload = function(e) {{
                    const base64Url = e.target.result;
                    uploadedPhotos.push(base64Url); // 存储到临时数组
                    // 生成预览图
                    addPreviewItem(base64Url);
                }};
                reader.readAsDataURL(file);
            }}
            // 清空文件选择框（否则无法重复选择同一文件）
            fileInput.value = '';
        }}

        /**
         * 添加图片预览项
         */
        function addPreviewItem(base64Url) {{
            const previewContainer = document.getElementById('uploadedPreview');
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            previewItem.innerHTML = `
                <img src="${{base64Url}}" alt="预览图">
                <button class="delete-btn" onclick="deletePreviewItem(this, '${{base64Url}}')">×</button>
            `;
            previewContainer.appendChild(previewItem);
        }}

        /**
         * 删除预览图片
         */
        function deletePreviewItem(btn, base64Url) {{
            // 从临时数组中移除
            uploadedPhotos = uploadedPhotos.filter(url => url !== base64Url);
            // 从DOM中移除预览项
            btn.parentElement.remove();
        }}

        // ========== 本地存储函数 ==========
        function loadDataFromStorage() {{
            const visitedStr = localStorage.getItem(STORAGE_KEY_VISITED);
            visitedPoints = visitedStr ? JSON.parse(visitedStr) : DEFAULT_VISITED;
            
            const wantStr = localStorage.getItem(STORAGE_KEY_WANT);
            wantToGoPoints = wantStr ? JSON.parse(wantStr) : DEFAULT_WANT;
        }}

        function saveDataToStorage() {{
            localStorage.setItem(STORAGE_KEY_VISITED, JSON.stringify(visitedPoints));
            localStorage.setItem(STORAGE_KEY_WANT, JSON.stringify(wantToGoPoints));
        }}

        function clearAllData() {{
            if (confirm('确定要清空所有数据吗？')) {{
                localStorage.removeItem(STORAGE_KEY_VISITED);
                localStorage.removeItem(STORAGE_KEY_WANT);
                uploadedPhotos = []; // 清空临时上传图片
                document.getElementById('uploadedPreview').innerHTML = '';
                loadDataFromStorage();
                refreshAllUI();
                alert('已清空所有数据');
            }}
        }}

        function resetToDefault() {{
            if (confirm('确定恢复默认数据吗？当前内容会被覆盖')) {{
                visitedPoints = JSON.parse(JSON.stringify(DEFAULT_VISITED));
                wantToGoPoints = JSON.parse(JSON.stringify(DEFAULT_WANT));
                uploadedPhotos = [];
                document.getElementById('uploadedPreview').innerHTML = '';
                saveDataToStorage();
                refreshAllUI();
                alert('已恢复默认数据');
            }}
        }}

        // ========== UI刷新函数 ==========
        function refreshAllUI() {{
            updateVisitedList();
            updateWantToGoList();
            initDescEditAndDisplay();
            renderAllMarkers();
        }}

        function updateVisitedList() {{
            const visitedListContent = document.getElementById('visitedListContent');
            visitedListContent.innerHTML = '';
            
            visitedPoints.forEach(place => {{
                const newItem = document.createElement('div');
                newItem.className = 'visited-place';
                newItem.dataset.place = place.name;
                newItem.textContent = place.name;
                
                // 点击显示照片（Base64格式）
                newItem.addEventListener('click', function() {{
                    const placeName = this.dataset.place;
                    document.getElementById('photoTitle').textContent = `${{placeName}}旅游照片`;
                    currentCityPhotos = visitedPoints.find(p => p.name === placeName)?.photos || [];
                    currentPhotoIndex = 0;
                    document.getElementById('photoBox').style.display = 'block';
                    updatePhotoDisplay();
                }});
                visitedListContent.appendChild(newItem);
            }});
        }}

        function updateWantToGoList() {{
            const wantToGoListContent = document.getElementById('wantToGoListContent');
            wantToGoListContent.innerHTML = '';
            
            wantToGoPoints.forEach(place => {{
                const newItem = document.createElement('div');
                newItem.className = 'want-to-go-item';
                newItem.textContent = place.name;
                wantToGoListContent.appendChild(newItem);
            }});
        }}

        function initDescEditAndDisplay() {{
            const descEditContainer = document.getElementById('descEditContainer');
            const descDisplayArea = document.getElementById('descDisplayArea');
            
            descEditContainer.innerHTML = '';
            descDisplayArea.innerHTML = '';
            
            visitedPoints.forEach(place => {{
                const descItem = document.createElement('div');
                descItem.className = 'desc-item';
                descItem.innerHTML = `
                    <h4>${{place.name}}</h4>
                    <textarea class="desc-textarea" data-place="${{place.name}}">${{place.desc || ''}}</textarea>
                    <button class="save-desc-btn" onclick="saveDesc('${{place.name}}')">保存</button>
                `;
                descEditContainer.appendChild(descItem);
                
                const displayItem = document.createElement('p');
                displayItem.className = 'desc-display';
                displayItem.id = `descDisplay_${{place.name}}`;
                displayItem.innerHTML = place.desc ? `${{place.name}}：${{place.desc}}` : `${{place.name}}：[点击上方编辑框填写介绍]`;
                descDisplayArea.appendChild(displayItem);
            }});
        }}

        function saveDesc(placeName) {{
            const textarea = document.querySelector(`.desc-textarea[data-place="${{placeName}}"]`);
            const newDesc = textarea.value.trim();
            
            const place = visitedPoints.find(p => p.name === placeName);
            if (place) place.desc = newDesc;
            
            saveDataToStorage();
            document.getElementById(`descDisplay_${{placeName}}`).innerHTML = `${{placeName}}：${{newDesc || '[点击上方编辑框填写介绍]'}}`;
            renderAllMarkers();
            alert(`已保存${{placeName}}的介绍`);
        }}

        // ========== 地图函数 ==========
        function initMap() {{
            if (map) return;
            map = new AMap.Map('footprintMap', {{
                zoom: 5,
                center: [105.0000, 30.0000]
            }});
            AMap.plugin(['AMap.ToolBar'], function() {{
                map.addControl(new AMap.ToolBar());
            }});
            renderAllMarkers();
        }}

        function renderAllMarkers() {{
            if (!map) return;
            mapMarkers.forEach(marker => map.remove(marker));
            mapMarkers = [];
            
            visitedPoints.forEach(point => {{
                const marker = new AMap.Marker({{
                    position: [point.lng, point.lat],
                    icon: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_r.png',
                    title: point.name
                }});
                map.add(marker);
                mapMarkers.push(marker);
                marker.on('click', function() {{
                    const infoWindow = new AMap.InfoWindow({{
                        content: `<div class="info-window"><h5>${{point.name}}</h5><p>${{point.desc || '暂无介绍'}}</p></div>`,
                        offset: new AMap.Pixel(0, -30)
                    }});
                    infoWindow.open(map, marker.getPosition());
                }});
            }});
            
            wantToGoPoints.forEach(point => {{
                const marker = new AMap.Marker({{
                    position: [point.lng, point.lat],
                    icon: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
                    title: point.name
                }});
                map.add(marker);
                mapMarkers.push(marker);
                marker.on('click', function() {{
                    const infoWindow = new AMap.InfoWindow({{
                        content: `<div class="info-window"><h5>${{point.name}}</h5><p>计划打卡</p></div>`,
                        offset: new AMap.Pixel(0, -30)
                    }});
                    infoWindow.open(map, marker.getPosition());
                }});
            }});
        }}

        // ========== 添加地点函数 ==========
        function addVisitedPlace() {{
            const name = document.getElementById('addVisitedName').value.trim();
            const lat = parseFloat(document.getElementById('addVisitedLat').value);
            const lng = parseFloat(document.getElementById('addVisitedLng').value);
            const desc = document.getElementById('addVisitedDesc').value.trim();
            
            // 验证输入
            if (!name || isNaN(lat) || isNaN(lng)) {{
                alert('请填写完整的地名、纬度、经度！');
                return;
            }}
            if (visitedPoints.some(p => p.name === name)) {{
                alert(`"${{name}}"已存在，请更换名称！`);
                return;
            }}

            // 组装地点数据（包含Base64图片）
            const newPlace = {{
                name: name,
                lat: lat,
                lng: lng,
                photos: [...uploadedPhotos], // 复制临时上传的图片
                desc: desc
            }};
            visitedPoints.push(newPlace);
            
            // 保存数据
            saveDataToStorage();
            refreshAllUI();
            
            // 重置输入和临时图片
            document.getElementById('addVisitedName').value = '';
            document.getElementById('addVisitedLat').value = '';
            document.getElementById('addVisitedLng').value = '';
            document.getElementById('addVisitedDesc').value = '';
            uploadedPhotos = [];
            document.getElementById('uploadedPreview').innerHTML = '';
            
            alert(`成功添加去过的地方：${{name}}`);
        }}

        function addWantToGoPlace() {{
            const name = document.getElementById('addWantName').value.trim();
            const lat = parseFloat(document.getElementById('addWantLat').value);
            const lng = parseFloat(document.getElementById('addWantLng').value);
            
            if (!name || isNaN(lat) || isNaN(lng)) {{
                alert('请填写完整的地名、纬度、经度！');
                return;
            }}
            if (wantToGoPoints.some(p => p.name === name)) {{
                alert(`"${{name}}"已存在，请更换名称！`);
                return;
            }}

            wantToGoPoints.push({{name, lat, lng}});
            saveDataToStorage();
            refreshAllUI();
            
            document.getElementById('addWantName').value = '';
            document.getElementById('addWantLat').value = '';
            document.getElementById('addWantLng').value = '';
            
            alert(`成功添加想去的地方：${{name}}`);
        }}

        // ========== 照片浏览函数 ==========
        function updatePhotoDisplay() {{
            const currentPhoto = document.getElementById('currentPhoto');
            const photoIndex = document.getElementById('photoIndex');
            const prevBtn = document.getElementById('prevBtn');
            const nextBtn = document.getElementById('nextBtn');
            
            if (currentCityPhotos.length === 0) {{
                currentPhoto.src = '';
                currentPhoto.alt = '暂无照片';
                photoIndex.textContent = '0/0';
                prevBtn.disabled = true;
                nextBtn.disabled = true;
                return;
            }}
            
            // 显示Base64格式的图片
            currentPhoto.src = currentCityPhotos[currentPhotoIndex];
            currentPhoto.alt = `${{document.getElementById('photoTitle').textContent}} - ${{currentPhotoIndex + 1}}`;
            photoIndex.textContent = `${{currentPhotoIndex + 1}}/${{currentCityPhotos.length}}`;
            prevBtn.disabled = currentPhotoIndex === 0;
            nextBtn.disabled = currentPhotoIndex === currentCityPhotos.length - 1;
        }}

        // ========== 页面交互函数 ==========
        function toggleDisplay(target, others) {{
            target.style.display = target.style.display === 'block' ? 'none' : 'block';
            others.forEach(el => el.style.display = 'none');
            if (target === document.getElementById('footprintArea')) {{
                initMap();
            }}
        }}

        // ========== 页面初始化 ==========
        window.onload = function() {{
            loadDataFromStorage();
            refreshAllUI();
            
            // 绑定按钮事件
            document.getElementById('visitedBtn').addEventListener('click', () => {{
                toggleDisplay(document.getElementById('visitedList'), [document.getElementById('wantToGoList'), document.getElementById('footprintArea')]);
                document.getElementById('photoBox').style.display = 'none';
            }});
            
            document.getElementById('wantToGoBtn').addEventListener('click', () => {{
                toggleDisplay(document.getElementById('wantToGoList'), [document.getElementById('visitedList'), document.getElementById('footprintArea')]);
                document.getElementById('photoBox').style.display = 'none';
            }});
            
            document.getElementById('footprintBtn').addEventListener('click', () => {{
                toggleDisplay(document.getElementById('footprintArea'), [document.getElementById('visitedList'), document.getElementById('wantToGoList')]);
                document.getElementById('photoBox').style.display = 'none';
            }});
            
            document.getElementById('prevBtn').addEventListener('click', function() {{
                if (currentPhotoIndex > 0) {{
                    currentPhotoIndex--;
                    updatePhotoDisplay();
                }}
            }});
            
            document.getElementById('nextBtn').addEventListener('click', function() {{
                if (currentPhotoIndex < currentCityPhotos.length - 1) {{
                    currentPhotoIndex++;
                    updatePhotoDisplay();
                }}
            }});
        }};
    </script>
</body>
</html>"""

    # 生成文件（添加错误捕获）
    try:
        # 确保目录存在
        if not os.path.exists(desktop_path):
            os.makedirs(desktop_path)
            print(f"✅ 已创建目录：{desktop_path}")
        
        # 生成HTML文件
        html_file_path = os.path.join(desktop_path, "旅游日记.html")
        with open(html_file_path, "w", encoding="utf-8", errors="ignore") as f:
            f.write(html_template)
        
        print(f"✅ 旅游日记网页已生成！")
        print(f"📂 文件路径：{html_file_path}")
        print(f"💡 现在支持直接上传图片，无需手动输入文件名")
    except Exception as e:
        print(f"❌ 生成失败：{str(e)}")

# 调用主函数
if __name__ == "__main__":

    generate_travel_diary()

