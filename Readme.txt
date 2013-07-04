汇联全景内容处理工具集

全景内容处理涉及的部门包括产品、摄影、修图、UI、编辑、开发部门，涉及到相关部门需要协助的任务直接找部门老大

当地消费模块数据生成流程：
1. 将数据模板文件夹life.template给到编辑，让编辑按照模板准备生活信息的数据
2. 运行generate_life_dev生成当地消费的开发用数据
> generate_life_dev life.template # 将生成life文件夹，即是开发用数据

全景内容准备流程
0. 将spots.xls表格分发相关人员填写
   先给到老卫填写景点，父景点及显示级别信息
   将老卫完成后的表格复制三份
   一份给到产品，填写出现于列表字段，写Y代表景点将出现于列表模式中
   一份给到编辑，填写景点说明及解说词字段（产品可以和编辑沟通哪些景点需要说明和解说词）
   一份给到摄影团队，填写全景图ID字段（此步请在步骤2后实施）
1. 汇总来自摄影团队的原始全景照片（摄影团队会将照片按照树形目录结构组织好）
2. 用脚本将树形目录结构转成水平结构（每一个目录将包含且只包含一个全景点的所有照片，目录名中将不再包含中文，每个目录都会加上一个编号），将水平结构的输出目录给到修图组拼接全景并修图
> flat_raw_dirs raw # raw是来自于摄影团队树形结构目录的根，输出的水平结构的目录将是raw.flat
> list_view_points raw.flat > list.txt # 将景点编号和景点路径的对应关系存到list.txt中给到摄影师填写spots.xls
3. 将raw.flat给到修图部门拼接和修图，完成后每个全景点将得到一张对应的全景图，全景图的名字跟拼接前目录的名字相同
4. 根据拼接好的全景图生成热点标注网站，
> make_pano_tour flat # 假设拼接好的全景根目录是flat，将会生成flat.tour的热点标注站
5. 将标注网站flat.tour给到摄影团队，让摄影团队标注热点，设定初始视角以及调整fov，完成后用他们导出的tour.xml覆盖flat.tour下的tour.xml
6. 生成开发用数据
> convert_tour_to_dev flat.tour # 将生成flat.dev目录，里面是开发用到的全景切图及json文件
7. 生成热点表格hsmap.xls给到产品，让产品部门安排人手填写hsmap.xls的image字段，image字段对应产品中看到的热点图标，不同类型的热点图标不同，所以要在表格中设定
> hotspots_mapping flat.dev # 将在当前目录下生hsmap.xls文件
8. 根据填写完毕的hsmap.xls往开发用数据中加入热点图片信息
> hotspots_mapping -a flat.dev # flat.dev中的json文件将被修改，注意hsmap.xls必须在当前目录下
9. 生分热点图片列表，给到UI让其设计热点图标
> list_hotspots_images hsmap.xls
10.为航拍全景数据添加name字段，假设此处用到的spots.xls已在之前准备好，假设flat.dev中航拍点的全景数据是a.json, b.json, c.json
> add_aerial_spots_name spots.xls flat.dev/a.json flat.dev/b.json flat.dev/c.json
11.将最终的flat.dev按开发的要求上传至服务器