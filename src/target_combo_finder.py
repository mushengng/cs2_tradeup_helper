import itertools        #专注于高效迭代器生成，提供一系列用于循环遍历、组合排列、无限迭代的工具函数，能简化循环逻辑并节省内存。应用了combinations函数
import decimal          #用于高精度十进制浮点运算，解决float类型的精度丢失问题。应用了Decimal类，ROUND_DOWN舍入模式常量
import math             #提供基础的数学运算函数，涵盖初等数学和部分高等数学功能。应用了comb函数


#获取decimal输入并进行合法性校验
def get_decimal_input(prompt, min_val = None, max_val = None, allow_equal = True):
                    #提示输入信息，最小值、最大值默认为空（可选），是否允许输入的数等于边界值

    while True:     #一直获取输入，直到获取一个符合要求的数
        try:        #捕获用户输入无法转换为decimal的异常（decimal.InvalidOperation），比如输入了字母、符号等非数字内容，这时提示用户重新输入，而不是让程序崩溃
            val_str = input(prompt).strip()     #提示输入信息prompt，获取输入并去除首尾空字符

            if not val_str:
                print("输入不能为空，请重新输入！")
                continue

            val = decimal.Decimal(val_str)      #转化为decimal精度类型

            #校验范围
            if min_val is not None:     #当最小值不是空时
                if allow_equal:     #如果允许等于边界值
                    if val < min_val:       #如果输入的数小于左边界
                        print(f"输入值不能小于{min_val}，请重新输入！")
                        continue
                else:       #如果不允许等于边界值
                    if val <= min_val:      #如果输入的数小于等于左边界
                        print(f"输入值必须大于{min_val}，请重新输入！")
                        continue

            if max_val is not None:     #与上同理
                if allow_equal:
                    if val > max_val:
                        print(f"输入值不能大于{max_val}，请重新输入！")
                        continue
                else:
                    if val >= max_val:
                        print(f"输入值必须小于{max_val}，请重新输入！")
                        continue

            return val      #返回输入的值

        except decimal.InvalidOperation:        #InvalidOperation是decimal模块定义的异常类，专门用于表示对Decimal类型进行操作时出现的无效运算错误
            print("输入不是有效的数字，请重新输入！")


#获取整数输入（用于指定匹配的小数位数）    与上同理
def get_int_input(prompt, min_val = 1, max_val = 17):
                #提示输入信息，最小值为1，最大值为17

    while True:     #一直获取输入，直到获取一个符合要求的数
        try:
            val_str = input(prompt).strip() #提示输入信息prompt，获取输入并去除首尾空字符

            if not val_str:
                print("输入不能为空，请重新输入！")
                continue

            val = int(val_str)  #转化为int类型

            if val < min_val or val > max_val:
                print(f"输入值必须在{min_val}到{max_val}之间，请重新输入！")
                continue

            return val

        except ValueError:      #通用异常类，触发场景是数据类型本身合法，但值不符合该类型的要求或操作的逻辑规则。即上方的转换失败
            print("输入不是有效的整数，请重新输入！")

#获取用户输入的材料磨损值和对应价格列表
def get_material_list(max_materials = 30):

    materials = []      #创建一个空列表，用于存储用户输入的所有材料信息，每个材料将用一个字典表示

    print(f"请输入材料磨损值（17位小数）和对应价格（格式：磨损值 价格，每行一组）：")
    print("示例：0.12345678901234567 100.5")
    print(f"最多可输入 {max_materials} 个材料，输入空行结束输入\n")

    idx = 0     #初始化一个计数器变量，用于记录当前是第几个材料，并且后续可以作为材料在原始输入顺序中的索引

    while idx < max_materials:      #当填入的材料数小于最大材料上限时允许一直填

        prompt = f"材料{idx + 1} / {max_materials} (磨损 价格，直接按Enter键结束): "       #创建提示字符串，显示当前是第几个材料并告诉用户填写格式

        line = input(prompt).strip()        #获取用户输入的一行内容

        if not line:        #若用户输入为空，即检查用户是否按了Enter
            if idx >= 10:       #若已经输入10个材料
                print(f"材料输入完成，共输入 {idx} 个材料")
                break
            else:
                print(f"至少需要10个材料，当前只有{idx}个，请继续输入")
                continue

        try:
            parts = line.split()        #把用户输入的一行内容按空白字符切割成多部分

            if len(parts) != 2:     #若没切割成两部分（即格式错误），回去重输
                print("输入格式错误，请使用'磨损值 价格'格式")
                continue

            wear = decimal.Decimal(parts[0])        #把第一部分转化成decimal类型存到变量wear中
            price = decimal.Decimal(parts[1])       #把第二部分转化成decimal类型存到变量price中

            if price < decimal.Decimal(0):       #这里因为price是decimal类型，要与0进行比较，需要先转换0的类型
                print("价格不能为负数，请重新输入")  #如果价格为负，回去重输
                continue

            materials.append({      #让先前73行创建的列表存放材料的字典信息
                "wear": wear,
                "price": price,
                "idx": idx
            })

            idx += 1        #材料计数加1

        except decimal.InvalidOperation:        #捕获decimal.InvalidOperation异常，当用户输入的字符串无法转化成decimal时触发
            print("磨损值格式错误，请输入17位小数格式")
        except Exception as e:      #捕获其他所有类型的异常并复制给e。Exception是所有内置非系统退出异常的基类
            print(f"输入错误: {e}")

    if len(materials) < 10:     #循环结束后，再次检查材料是否足够
        print(f"至少需要10个材料，当前只有{len(materials)}个")
        return None

    return materials

#将decimal数值截断到指定小数位数
def truncate_decimal(value, decimal_places):
                #要截断的十进制数，要保留的小数位数

    if decimal_places <= 0:     #如果要保留的小数位比0小
        return decimal.Decimal(int(value))      #则直接返回整数部分

    factor = decimal.Decimal(10) ** decimal_places      #创建一个因子，若保留的小数位是3，则factor=10的3次方
    truncated = (value * factor).to_integral_value(rounding=decimal.ROUND_DOWN) / factor
                #先将数字乘因子，这样得到的就是保留小数位扩大到整数部分，再进行向下取整，清除后面的小数位，再除以因子回到正确的数字
    return truncated


#计算产物的最终磨损值
def calculate_product_wear(combo, m_min, m_max, p_min, p_max):
                    #十个材料的组合（是一个列表），材料最小磨损，材料最大磨损，产物最小磨损，产物最大磨损

    total_normalized = decimal.Decimal('0')     #初始化一个decimal类型的变量，用于累加所有材料的归一化磨损值

    for mat in combo:       #遍历组合（一个列表）中的每个材料（一个字典）
        normalized = (mat["wear"] - m_min) / (m_max - m_min)        #计算单个材料的归一化磨损
        total_normalized += normalized      #求和

    avg_normalized = total_normalized / decimal.Decimal('10')       #十个材料的归一化磨损求均值
    product_wear = p_min + avg_normalized * (p_max - p_min)     #产物磨损计算公式

    return product_wear


#搜索所有符合条件的组合
def find_all_combinations(materials, target_wear, m_min, m_max, p_min, p_max, match_decimals):
                    #材料列表，目标磨损，材料最小磨损，材料最大磨损，产物最小磨损，产物最大磨损，需要匹配的小数位数

    results = []        #初始化一个空列表，用于存放所有符合条件的组合

    #把目标值截断到指定小数位数
    target_wear_truncated = truncate_decimal(target_wear, match_decimals)

    #计算总组合数
    n = len(materials)
    total_combos = math.comb(n, 10)
    print(f"需要搜索 {total_combos:,} 种组合...")

    #预计算每个材料的归一化磨损值，提高性能
    for mat in materials:
        mat["normalized"] = (mat["wear"] - m_min) / (m_max - m_min)

    #初始化两个计数器
    processed = 0       #用于计数已处理的组合数
    found_count = 0     #用于计数已找到的符合条件的组合数

    #使用itertools.combinations迭代器遍历所有10个材料的组合
    for combo in itertools.combinations(materials, 10):

        processed += 1

        #显示进度
        if processed % 100000 == 0:     #每处理十万次输出进度信息
            print(f"已处理 {processed:,} 种组合...")

        #计算产物磨损值
        product_wear = p_min + (sum(mat["normalized"] for mat in combo) / decimal.Decimal('10')) * (p_max - p_min)

        #将计算结果截断到指定小数位数
        product_wear_truncated = truncate_decimal(product_wear, match_decimals)

        #比较截断后的值
        if product_wear_truncated == target_wear_truncated:
            total_price = sum(mat["price"] for mat in combo)        #计算该组合的总价

            #保持组合内材料的原始顺序（用户输入顺序）
            sorted_combo = sorted(combo, key=lambda x: x["idx"])        #对从itertools.combinations生成的10个材料组合（combo），按照每个材料的 "idx" 值（用户输入材料时的原始顺序编号）进行升序排序，生成一个新的排序后的列表并赋值给sorted_combo
                                   #lambda是Python中定义匿名函数的关键字    #即把combo内部的十个字典按照字典里的idx排序

            #把符合条件的组合信息添加到结果列表中（161行）
            results.append({
                "combo": sorted_combo,
                "total_price": total_price,
                "product_wear": product_wear
            })      #results是一个列表，其中的每一个元素都是一个字典，而这个字典的键（元素）combo又是一个列表，包含着十个材料的信息，该信息又是一个字典

            found_count += 1

    return results


#主函数
def main():
    #设置decimal的精度为50位小数，确保17位小数计算准确
    decimal.getcontext().prec = 50

    print("=" * 40)
    print("磨损组合计算程序")
    print("=" * 40)

    #1.输入材料的最小/最大磨损值
    print("\n【第一步】请输入材料磨损范围：")
    m_min = get_decimal_input("材料最小磨损值：", allow_equal=True)
    m_max = get_decimal_input("材料最大磨损值：", min_val=m_min, allow_equal=False)

    #2.输入产物的最小/最大磨损值
    print("\n【第二步】请输入产物磨损范围：")
    p_min = get_decimal_input("产物最小磨损值：", allow_equal=True)
    p_max = get_decimal_input("产物最大磨损值：", min_val=p_min, allow_equal=False)

    #3.输入目标最终磨损值
    print("\n【第三步】请输入目标最终磨损值：")
    target_wear = get_decimal_input("目标最终磨损值：",min_val=p_min,max_val=p_max,allow_equal=True)

    #4.输入需要匹配的小数位数
    print("\n【第四步】请输入需要匹配的小数位数：")
    match_decimals = get_int_input("需要匹配的小数位数（1-17）：", min_val=1, max_val=17)
    print(f"将按「截断到{match_decimals}位小数」的规则匹配组合！")

    #5.输入材料列表
    print("\n【第五步】请输入材料列表（最多30个材料）：")
    materials = get_material_list(max_materials=30)

    if not materials:   #材料为空
        return

    #检查材料数量
    n = len(materials)
    if n > 30:
        print(f"警告：材料数量超过30个，只使用前30个材料")
        materials = materials[:30]  #截断前30个
        n = 30

    #6.显示目标值
    target_wear_truncated = truncate_decimal(target_wear, match_decimals)
    print(f"\n目标最终磨损值: {target_wear}")
    print(f"目标值截断到{match_decimals}位小数后: {target_wear_truncated:.{match_decimals}f}")
    print(f"材料数量: {n}")

    #7.搜索符合条件的组合
    print(f"\n【第六步】开始查找符合条件的组合...")

    #计算总组合数
    total_combos = math.comb(n, 10)
    print(f"总组合数: C({n}, 10) = {total_combos:,}")

    if total_combos > 10000000:
        print("警告：组合数量较大，搜索可能需要较长时间！")
        print("请耐心等待...")

    #搜索所有组合
    matched_combinations = find_all_combinations(materials, target_wear, m_min, m_max, p_min, p_max, match_decimals)
    print(f"搜索完成，找到 {len(matched_combinations)} 个符合条件的组合")

    #8.处理结果
    if not matched_combinations:
        print(f"\n未找到「截断到{match_decimals}位小数后」符合要求的10个材料组合！")
        return

    #按总价格升序排序
    matched_combinations.sort(key=lambda x: x["total_price"])

    #9.输出前10个价格最低的组合
    print(f"\n" + "=" * 40)
    print(f"前10个价格最低的组合（按总价格升序）：")
    print("=" * 40)

    for i, result in enumerate(matched_combinations[:10], 1):       #enumerate用于将一个可迭代对象组合为一个索引序列，用于在循环中同时获取索引和元素值
                                #取前十个组合
                    #enumerate生成索引和元素的配对，索引从1开始

        #从结果中提取组合数据
        combo = result["combo"]
        total_price = result["total_price"]
        product_wear = result["product_wear"]

        print(f"\n组合 {i}: 总价格 = {total_price:.2f}")
        print("-" * 40)
        print(f"{'材料编号':<14}{'磨损值':<18}{'价格':<10}")     #左对齐，宽度14个字符

        #按用户输入顺序输出
        for mat in combo:
            print(f"{mat['idx'] + 1:<10}{mat['wear']:<27}{mat['price']:<12.2f}")

        #显示计算结果（17位小数）
        print(f"计算结果: {product_wear:.17f}")


try:
    main()
except KeyboardInterrupt:       #KeyboardInterrupt是Python内置的中断类异常，专门用于表示“程序运行时被用户手动中断”的情况
    print("\n程序被用户中断")
except Exception as e:      #捕获其他所有类型的异常并复制给e。Exception是所有内置非系统退出异常的基类
    print(f"程序运行出错: {e}")