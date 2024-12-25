#include "myglwidget.h"
#include <GL/glew.h>
#include <algorithm>
#include <chrono>

MyGLWidget::MyGLWidget(QWidget *parent)
	:QOpenGLWidget(parent)
{
}

MyGLWidget::~MyGLWidget()
{
	delete[] render_buffer;
	delete[] temp_render_buffer;
	delete[] temp_z_buffer;
	delete[] z_buffer;
}

void MyGLWidget::resizeBuffer(int newW, int newH) {
	delete[] render_buffer;
	delete[] temp_render_buffer;
	delete[] temp_z_buffer;
	delete[] z_buffer;
	WindowSizeW = newW;
	WindowSizeH = newH;
	render_buffer = new vec3[WindowSizeH*WindowSizeW];
	temp_render_buffer = new vec3[WindowSizeH*WindowSizeW];
	temp_z_buffer = new float[WindowSizeH*WindowSizeW];
	z_buffer = new float[WindowSizeH*WindowSizeW];
}

void MyGLWidget::initializeGL()
{
	WindowSizeW = width();
	WindowSizeH = height();
	glViewport(0, 0, WindowSizeW, WindowSizeH);
	glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
	glDisable(GL_DEPTH_TEST);
	offset = vec2(WindowSizeH / 2, WindowSizeW / 2);
	// 对定义的数组初始化
	render_buffer = new vec3[WindowSizeH*WindowSizeW];
	temp_render_buffer = new vec3[WindowSizeH*WindowSizeW];
	temp_z_buffer = new float[WindowSizeH*WindowSizeW];
	z_buffer = new float[WindowSizeH*WindowSizeW];
	for (int i = 0; i < WindowSizeH*WindowSizeW; i++) {
		render_buffer[i] = vec3(0, 0, 0);
		temp_render_buffer[i] = vec3(0, 0, 0);
		temp_z_buffer[i] = MAX_Z_BUFFER;			
		z_buffer[i] = MAX_Z_BUFFER;
	}
}

void MyGLWidget::keyPressEvent(QKeyEvent *e) {
	
	switch (e->key()) {
		case Qt::Key_0: scene_id = 0;update(); break;
		case Qt::Key_1: scene_id = 1;update(); break;
		case Qt::Key_8: degree -= 30;update(); break;
		case Qt::Key_9: degree += 30;update(); break;
	}
}

void MyGLWidget::paintGL()
{
	auto start_time = std::chrono::high_resolution_clock::now();
	switch (scene_id) {
		case 0:scene_0(); break;
		case 1:scene_1(); break;
	}
	auto end_time = std::chrono::high_resolution_clock::now();
	auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
	std::cout << "Time taken: " << duration.count() << " milliseconds" << std::endl;
}

void MyGLWidget::clearBuffer(vec3* now_buffer) {
	for (int i = 0; i < WindowSizeH*WindowSizeW; i++) {
		now_buffer[i] = vec3(0,0,0);
	}
}

void MyGLWidget::clearBuffer(int* now_buffer) {
	memset(now_buffer, 0, WindowSizeW * WindowSizeH * sizeof(int));
}

void MyGLWidget::clearZBuffer(float* now_buffer) {
	std::fill(now_buffer,now_buffer+WindowSizeW * WindowSizeH, MAX_Z_BUFFER);
}

// 窗口大小变动后，需要重新生成render_buffer等数组
void MyGLWidget::resizeGL(int w, int h)
{
	resizeBuffer(w, h);
	offset = vec2(WindowSizeW / 2, WindowSizeH / 2);
	clearBuffer(render_buffer);
}

void MyGLWidget::scene_0()
{
	// 选择要加载的model
	objModel.loadModel("./objs/singleTriangle.obj");

	// 自主设置变换矩阵
	camPosition = vec3(100 * sin(degree * 3.14 / 180.0) + objModel.centralPoint.x, 100 * cos(degree * 3.14 / 180.0) + objModel.centralPoint.y, 10+ objModel.centralPoint.z);
	camLookAt = objModel.centralPoint;     // 例如，看向物体中心
	camUp = vec3(0, 1, 0);         // 上方向向量
	projMatrix = glm::perspective(radians(20.0f), 1.0f, 0.1f, 2000.0f);

	// 单一点光源，可以改为数组实现多光源
	lightPosition = objModel.centralPoint + vec3(0,100,100);
	clearBuffer(render_buffer);
	clearZBuffer(z_buffer);
	for (int i = 0; i < objModel.triangleCount; i++) {
		Triangle nowTriangle = objModel.getTriangleByID(i);
		drawTriangle(nowTriangle);
	}
	glClear(GL_COLOR_BUFFER_BIT);
	renderWithTexture(render_buffer,WindowSizeH,WindowSizeW);
}

void MyGLWidget::scene_1()
{
	// 选择要加载的model
	// objModel.loadModel("./objs/teapot_600.obj");
	objModel.loadModel("./objs/teapot_8000.obj");
	//objModel.loadModel("./objs/rock.obj");
	//objModel.loadModel("./objs/cube.obj");
	//objModel.loadModel("./objs/singleTriangle.obj");
	
	// 自主设置变换矩阵
	camPosition = vec3(100 * sin(degree * 3.14 / 180.0) + objModel.centralPoint.x, 100 * cos(degree * 3.14 / 180.0) + objModel.centralPoint.y, 10+ objModel.centralPoint.z);
	camLookAt = objModel.centralPoint;     // 例如，看向物体中心
	camUp = vec3(0, 1, 0);         // 上方向向量
	projMatrix = glm::perspective(radians(25.0f), 1.0f, 0.1f, 2000.0f);

	// 单一点光源，可以改为数组实现多光源
	lightPosition = objModel.centralPoint + vec3(0,100,100);
	clearBuffer(render_buffer);
	clearZBuffer(z_buffer);
	for (int i = 0; i < objModel.triangleCount; i++) {
		Triangle nowTriangle = objModel.getTriangleByID(i);
		drawTriangle(nowTriangle);
	}
	glClear(GL_COLOR_BUFFER_BIT);
	renderWithTexture(render_buffer, WindowSizeH, WindowSizeW);
}

void MyGLWidget::drawTriangle(Triangle triangle) {
	// 三维顶点映射到二维平面
	vec3* vertices = triangle.triangleVertices;
	vec3* normals = triangle.triangleNormals;
	FragmentAttr transformedVertices[3];
	clearBuffer(this->temp_render_buffer);
	clearZBuffer(this->temp_z_buffer);
	mat4 viewMatrix = glm::lookAt(camPosition, camLookAt, camUp);

    for (int i = 0; i < 3; ++i) {
		vec4 ver_mv = viewMatrix * vec4(vertices[i], 1.0f);
		float nowz = glm::length(camPosition - vec3(ver_mv));
		vec4 ver_proj = projMatrix * ver_mv;
		transformedVertices[i].x = ver_proj.x + offset.x;
		transformedVertices[i].y = ver_proj.y + offset.y;
		transformedVertices[i].z = nowz;
		transformedVertices[i].pos_mv = ver_mv;  
		mat3 normalMatrix = mat3(viewMatrix);
		vec3 normal_mv = normalMatrix * normals[i];
		transformedVertices[i].normal = normal_mv;
		if (shadingMode == GOURAUD) {
			transformedVertices[i].color = calculateVertexLighting(transformedVertices[i].pos_mv, transformedVertices[i].normal);
		}
    }

	// 将当前三角形渲染在temp_buffer中
		
	// HomeWork: 1、绘制三角形三边
	switch (drawMode) {
	case DDA:
		dda(transformedVertices[0], transformedVertices[1], 1);
    	dda(transformedVertices[1], transformedVertices[2], 2);
    	dda(transformedVertices[2], transformedVertices[0], 3);
		break;
	case BRESENHAM:
		bresenham(transformedVertices[0], transformedVertices[1], 1);
    	bresenham(transformedVertices[1], transformedVertices[2], 2);
    	bresenham(transformedVertices[2], transformedVertices[0], 3);
		break;
	}

    // HomeWork: 2: 用edge-walking填充三角形内部到temp_buffer中
	if (shadingMode != NONE) {
    	edge_walking(transformedVertices);
	}

	// 合并temp_buffer 到 render_buffer, 深度测试
	// 从firstChangeLine开始遍历，可以稍快
	for(int h = 0; h < WindowSizeH ; h++){
		auto render_row = &render_buffer[h * WindowSizeW];
		auto temp_render_row = &temp_render_buffer[h * WindowSizeW];
		auto z_buffer_row = &z_buffer[h*WindowSizeW];
		auto temp_z_buffer_row = &temp_z_buffer[h*WindowSizeW];
		for (int i = 0 ; i < WindowSizeW ; i++){
			if (z_buffer_row[i] < temp_z_buffer_row[i])
				continue;
			else
			{
				z_buffer_row[i] = temp_z_buffer_row[i];
				render_row[i] = temp_render_row[i];
			}
		}
	}
}

void MyGLWidget::dda(FragmentAttr& start, FragmentAttr& end, int id) {
	float x0 = start.x, x1 = end.x;
	float y0 = start.y, y1 = end.y;
	float z0 = start.z, z1 = end.z;

	float dx = x1 - x0;
	float dy = y1 - y0;
	float dz = z1 - z0;

	if (dx == 0 && dy == 0)
		return ;

	float steps = max(abs(dx), abs(dy));

	float xIncrement = dx / steps;
	float yIncrement = dy / steps;
	float zIncrement = dz / steps;

	float x = x0;
	float y = y0;
	float z = z0;

	for (int i = 0; i < steps; ++i) {
		if (x < 0 || x >= WindowSizeW || y < 0 || y >= WindowSizeH)
			return /* Do Nothing */;

		int index = (int)y * WindowSizeW + (int)x;	
		if (temp_z_buffer[index] > z) {
			temp_z_buffer[index] = z;
			temp_render_buffer[index] = lineColor;
		}
		x += xIncrement;
		y += yIncrement;
		z += zIncrement;
	}
}

void MyGLWidget::bresenham(FragmentAttr& start, FragmentAttr& end, int id) {
	int x0 = start.x, x1 = end.x;
	int y0 = start.y, y1 = end.y;
	float z0 = start.z, z1 = end.z;

	int dx = abs(x1 - x0);
  	int dy = abs(y1 - y0);

	if (dx == 0 && dy == 0) 
		return ; 

  	int sx = (x0 < x1) ? 1 : -1;
  	int sy = (y0 < y1) ? 1 : -1;
	int err = dx - dy;

	float steps = max(dx, dy);
	float zIncrement = (z1 - z0) / steps;

	int x = x0;
	int y = y0;
	float z = z0;

	while (x != x1 || y != y1) {

		if (x < 0 || x >= WindowSizeW || y < 0 || y >= WindowSizeH)
			return /* Do Nothing */;

		int index = y * WindowSizeW + x;
		if (temp_z_buffer[index] > z) {
			temp_z_buffer[index] = z;
			temp_render_buffer[index] = lineColor;
		}
		int e2 = 2 * err;
		if (e2 > -dy) { err -= dy; x += sx; }
		if (e2 < dx) { err += dx; y += sy; }
		z += zIncrement;
	}
}

void MyGLWidget::edge_walking(FragmentAttr* transformedVertices) {
	std::vector<std::vector<std::pair<int, float>>> edge_table(WindowSizeH);

	for (int y = 0; y < WindowSizeH; ++y) {
		for (int x = 0; x < WindowSizeW; ++x) {
			int index = y * WindowSizeW + x;
			if (temp_render_buffer[index] != vec3(0.0, 0.0, 0.0))
				edge_table[y].push_back({x, temp_z_buffer[index]});
		}
	}

	for (int y = 0; y < WindowSizeH; ++y) {
        if (edge_table[y].size() >= 2) {
            std::sort(edge_table[y].begin(), edge_table[y].end());
            
            for (size_t i = 0; i < edge_table[y].size() - 1; ++i) {
				int x_start = edge_table[y][i].first;
                int x_end = edge_table[y][i + 1].first;
                float z_start = edge_table[y][i].second;
                float z_end = edge_table[y][i + 1].second;

				if (x_start == x_end) continue;

				for (int x = x_start + 1; x < x_end; ++x) {
					int index = y * WindowSizeW + x;	

					float t = (float)(x - x_start) / (x_end - x_start);
					float interpolated_z = z_start + t * (z_end - z_start);
					temp_z_buffer[index] = interpolated_z;

					switch(shadingMode) {
					case GOURAUD:
						temp_render_buffer[index] = GouraudShading(x, y, transformedVertices);
						break;
					case PHONG:
						temp_render_buffer[index] = PhongShading(x, y, transformedVertices);
						break;
					case BLINN_PHONG:
						temp_render_buffer[index] = BlinnPhongShading(x, y, transformedVertices);
						break;
					default:
						temp_render_buffer[index] = objectColor;
					}
				}
			}
		}
	}
}

void MyGLWidget::calculateBarycentricCoordinates(int x, int y, FragmentAttr* v, float& alpha, float& beta, float& gamma) {
    vec2 p(x, y);
    vec2 a(v[0].x, v[0].y);
    vec2 b(v[1].x, v[1].y);
    vec2 c(v[2].x, v[2].y);

    vec2 v0 = b - a, v1 = c - a, v2 = p - a;
    float d00 = dot(v0, v0);
    float d01 = dot(v0, v1);
    float d11 = dot(v1, v1);
    float d20 = dot(v2, v0);
    float d21 = dot(v2, v1);
    float denom = d00 * d11 - d01 * d01;

    beta = (d11 * d20 - d01 * d21) / denom;
    gamma = (d00 * d21 - d01 * d20) / denom;
    alpha = 1.0f - beta - gamma;
}

vec3 MyGLWidget::calculateVertexLighting(const vec3& position, const vec3& normal) {
    vec3 norm = normalize(normal);
    vec3 lightDir = normalize(lightPosition - position);
    vec3 viewDir = normalize(camPosition - position);
    vec3 reflectDir = reflect(-lightDir, norm);

    // 环境光
    vec3 ambient = ambientStrength * lightColor;

    // 漫反射
    float diff = max(dot(norm, lightDir), 0.0f);
    vec3 diffuse = diff * lightColor;

    // 镜面反射
    float spec = pow(max(dot(viewDir, reflectDir), 0.0f), 32);
    vec3 specular = specularStrength * spec * lightColor;

    // 合并结果
    vec3 result = (ambient + diffuse + specular) * objectColor;
    return result;
}

vec3 MyGLWidget::GouraudShading(int x, int y, FragmentAttr* v) {
    float alpha, beta, gamma;
    calculateBarycentricCoordinates(x, y, v, alpha, beta, gamma);

    // Interpolate vertex colors (assuming they were calculated earlier)
    vec3 color = alpha * v[0].color + beta * v[1].color + gamma * v[2].color;
    return color;
}

vec3 MyGLWidget::PhongShading(int x, int y, FragmentAttr* v) {
    float alpha, beta, gamma;
    calculateBarycentricCoordinates(x, y, v, alpha, beta, gamma);

    // Interpolate position and normal
    vec3 position = alpha * vec3(v[0].pos_mv) + beta * vec3(v[1].pos_mv) + gamma * vec3(v[2].pos_mv);
    vec3 normal = normalize(alpha * v[0].normal + beta * v[1].normal + gamma * v[2].normal);

    // Calculate lighting
    vec3 lightDir = normalize(lightPosition - position);
    vec3 viewDir = normalize(camPosition - position);
    vec3 reflectDir = reflect(-lightDir, normal);

    // Ambient
    vec3 ambient = ambientStrength * lightColor;

    // Diffuse
    float diff = max(dot(normal, lightDir), 0.0f);
    vec3 diffuse = diff * lightColor;

    // Specular
    float spec = pow(max(dot(viewDir, reflectDir), 0.0f), 32);
    vec3 specular = specularStrength * spec * lightColor;

    // Combine results
    vec3 result = (ambient + diffuse + specular) * objectColor;
    return result;
}

vec3 MyGLWidget::BlinnPhongShading(int x, int y, FragmentAttr* v) {
    float alpha, beta, gamma;
    calculateBarycentricCoordinates(x, y, v, alpha, beta, gamma);

    // Interpolate position and normal
    vec3 position = alpha * vec3(v[0].pos_mv) + beta * vec3(v[1].pos_mv) + gamma * vec3(v[2].pos_mv);
    vec3 normal = normalize(alpha * v[0].normal + beta * v[1].normal + gamma * v[2].normal);

    // Calculate lighting
    vec3 lightDir = normalize(lightPosition - position);
    vec3 viewDir = normalize(camPosition - position);
    vec3 halfwayDir = normalize(lightDir + viewDir);

    // Ambient
    vec3 ambient = ambientStrength * lightColor;

    // Diffuse
    float diff = max(dot(normal, lightDir), 0.0f);
    vec3 diffuse = diff * lightColor;

    // Specular
    float spec = pow(max(dot(normal, halfwayDir), 0.0f), 64);
    vec3 specular = specularStrength * spec * lightColor;

    // Combine results
    vec3 result = (ambient + diffuse + specular) * objectColor;
    return result;
}