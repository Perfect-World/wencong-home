import zipfile, shutil, re, os, tempfile
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# ========== 1. 读源数据 ==========
src = load_workbook('01-需求与预算/装修控价表.xlsx')
ws_y_old = src['硬装半包费用']
ws_z_old = src['主材费用']
ws_r_old = src['家居家电费用']

y_rows = []
for r in range(2, ws_y_old.max_row + 1):
    t = ws_y_old.cell(r,1).value
    item = ws_y_old.cell(r,2).value
    if t and str(t).strip() and item and str(item).strip():
        y_rows.append([ws_y_old.cell(r,c).value for c in range(1,7)])
y_groups, seen = [], {}
for row in y_rows:
    g = str(row[0]).strip()
    if g not in seen:
        seen[g] = []; y_groups.append((g, seen[g]))
    seen[g].append(row)

z_rows = []
for r in range(3, ws_z_old.max_row + 1):
    v = [ws_z_old.cell(r,c).value for c in range(1,12)]
    if any(x not in (None,'') for x in v): z_rows.append(v)
r_rows = []
for r in range(3, ws_r_old.max_row + 1):
    v = [ws_r_old.cell(r,c).value for c in range(1,10)]
    if any(x not in (None,'') for x in v): r_rows.append(v)

# ========== 2. 样式 ==========
HFILL = PatternFill('solid', fgColor='1F4E78')
TFILL = PatternFill('solid', fgColor='EAF2FF')
SFILL = PatternFill('solid', fgColor='F0F4FA')
Z1 = PatternFill('solid', fgColor='FFFFFF')
Z2 = PatternFill('solid', fgColor='F7F9FC')
NOR = Font(size=11, name='Arial', color='1F2937')
CTR = Alignment(horizontal='center', vertical='center', wrap_text=True)
LFT = Alignment(horizontal='left', vertical='center', wrap_text=True)
RGT = Alignment(horizontal='right', vertical='center')
THIN = Side(style='thin', color='D9DEE7')
MED = Side(style='medium', color='AAB4C5')
TB = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
TB_TOP = Border(left=THIN, right=THIN, top=MED, bottom=THIN)

def LNK(cell, target):
    cell.hyperlink = target  # 先随便写，后面修 XML
    cell.font = Font(bold=True, size=11, name='Arial', color='1F6FEB', underline='single')

# ========== 3. 新建 ==========
wb = Workbook()

# --- 硬装 ---
ws1 = wb.active; ws1.title = '硬装'
cols = ['类型', '施工项目', '区域', '数量', '单价（元）', '总价（元）']
for ci, c in enumerate(cols, 1):
    cell = ws1.cell(1, ci, c)
    cell.font = Font(bold=True, color='FFFFFF', size=14, name='Arial')
    cell.fill = HFILL; cell.alignment = CTR; cell.border = TB
cur = 2
group_sub_rows = {}
for gname, grows in y_groups:
    g_start = cur
    for row in grows:
        for j, v in enumerate(row): ws1.cell(cur, j+1, v)
        fill = Z1 if (cur - 2) % 2 == 0 else Z2
        for c in range(1, 7):
            cc = ws1.cell(cur, c)
            cc.fill = fill; cc.border = TB
            cc.alignment = LFT if c <= 3 else CTR; cc.font = NOR
        ws1.cell(cur, 5).number_format = '¥#,##0'
        ws1.cell(cur, 6).number_format = '¥#,##0'
        cur += 1
    g_end = cur - 1
    ws1.cell(cur, 1, f'【{gname}】小计')
    ws1.cell(cur, 6, f'=SUM(F{g_start}:F{g_end})')
    group_sub_rows[gname] = cur
    for c in range(1, 7):
        cc = ws1.cell(cur, c)
        cc.fill = SFILL; cc.border = TB; cc.alignment = CTR
        cc.font = Font(bold=True, size=11, name='Arial', color='374151')
    ws1.cell(cur, 6).number_format = '¥#,##0'
    cur += 1
y_total = cur
ws1.cell(y_total, 1, '硬装总计')
ws1.cell(y_total, 6, f'=SUM(F2:F{y_total-1})')
for c in range(1, 7):
    cc = ws1.cell(y_total, c)
    cc.fill = TFILL; cc.border = TB_TOP; cc.alignment = CTR
    cc.font = Font(bold=True, size=14, name='Arial', color='1F2937')
ws1.cell(y_total, 6).number_format = '¥#,##0'
for col, w in zip('ABCDEF', [12, 28, 20, 10, 14, 16]):
    ws1.column_dimensions[col].width = w
ws1.freeze_panes = 'A2'

# --- 主材 ---
ws2 = wb.create_sheet('主材')
cols_z = ['类别', '名称', '区域', '品牌', '数量', '单价', '运费', '实采总价', '备注', '是否下单', '购买时间']
for ci, c in enumerate(cols_z, 1):
    cell = ws2.cell(1, ci, c)
    cell.font = Font(bold=True, color='FFFFFF', size=14, name='Arial')
    cell.fill = HFILL; cell.alignment = CTR; cell.border = TB
for i, row in enumerate(z_rows):
    for j, v in enumerate(row): ws2.cell(2+i, j+1, v)
    fill = Z1 if (2+i-2) % 2 == 0 else Z2
    for c in range(1, 12):
        cc = ws2.cell(2+i, c)
        cc.fill = fill; cc.border = TB
        cc.alignment = LFT if c <= 4 or c >= 9 else CTR; cc.font = NOR
        if c in (6,7,8): cc.number_format = '¥#,##0'
z_total = 2 + len(z_rows)
ws2.cell(z_total, 1, '主材总计')
ws2.cell(z_total, 8, f'=SUM(H2:H{z_total-1})')
for c in range(1, 12):
    cc = ws2.cell(z_total, c)
    cc.fill = TFILL; cc.border = TB_TOP; cc.alignment = CTR
    cc.font = Font(bold=True, size=14, name='Arial', color='1F2937')
ws2.cell(z_total, 8).number_format = '¥#,##0'
for i, w in enumerate([10,18,14,14,8,12,10,14,14,10,14], 1):
    ws2.column_dimensions[chr(64+i) if i<=26 else 'A'+chr(64+i-26)].width = w
ws2.freeze_panes = 'A2'

# --- 软装 ---
ws3 = wb.create_sheet('软装')
cols_r = ['类别', '区域', '名称', '品牌', '数量', '单价', '实采总价', '是否下单', '备注']
for ci, c in enumerate(cols_r, 1):
    cell = ws3.cell(1, ci, c)
    cell.font = Font(bold=True, color='FFFFFF', size=14, name='Arial')
    cell.fill = HFILL; cell.alignment = CTR; cell.border = TB
for i, row in enumerate(r_rows):
    for j, v in enumerate(row): ws3.cell(2+i, j+1, v)
    fill = Z1 if (2+i-2) % 2 == 0 else Z2
    for c in range(1, 10):
        cc = ws3.cell(2+i, c)
        cc.fill = fill; cc.border = TB
        cc.alignment = LFT if c <= 4 or c >= 8 else CTR; cc.font = NOR
        if c in (6,7): cc.number_format = '¥#,##0'
r_total = 2 + len(r_rows)
ws3.cell(r_total, 1, '软装总计')
ws3.cell(r_total, 7, f'=SUM(G2:G{r_total-1})')
for c in range(1, 10):
    cc = ws3.cell(r_total, c)
    cc.fill = TFILL; cc.border = TB_TOP; cc.alignment = CTR
    cc.font = Font(bold=True, size=14, name='Arial', color='1F2937')
ws3.cell(r_total, 7).number_format = '¥#,##0'
for i, w in enumerate([14,10,18,18,8,12,14,10,14], 1):
    ws3.column_dimensions[chr(64+i)].width = w
ws3.freeze_panes = 'A2'

# ========== 总控 ==========
ws0 = wb.create_sheet('总控', 0)
ws0.merge_cells('A1:K1')
ws0['A1'] = '装修预算总控'
ws0['A1'].font = Font(bold=True, size=22, name='Arial', color='1F2937')
ws0['A1'].alignment = CTR

# 预算表
bh = ['类别', '预算 (¥)', '占比', '实际花费 (¥)', '消耗进度', '结余 (¥)']
for ci, c in enumerate(bh, 1):
    cell = ws0.cell(3, ci, c)
    cell.font = Font(bold=True, color='FFFFFF', size=14, name='Arial')
    cell.fill = HFILL; cell.alignment = CTR; cell.border = TB

rows_info = [
    ('硬装', 68000, f"'硬装'!F{y_total}"),
    ('主材', 50555, f"'主材'!H{z_total}"),
    ('软装', 99999, f"'软装'!G{r_total}"),
]
for i, (name, budget, ref) in enumerate(rows_info, 4):
    ws0.cell(i, 1, name)
    ws0.cell(i, 2, budget); ws0.cell(i, 2).number_format = '¥#,##0'
    ws0.cell(i, 3, f'=B{i}/B7'); ws0.cell(i, 3).number_format = '0.0%'
    ws0.cell(i, 4, f'={ref}'); ws0.cell(i, 4).number_format = '¥#,##0'
    ws0.cell(i, 5, f'=IF(B{i}=0,0,D{i}/B{i})'); ws0.cell(i, 5).number_format = '0.0%'
    ws0.cell(i, 6, f'=B{i}-D{i}'); ws0.cell(i, 6).number_format = '¥#,##0'

ws0.cell(7, 1, '总计')
ws0.cell(7, 2, '=SUM(B4:B6)')
ws0.cell(7, 4, '=SUM(D4:D6)')
ws0.cell(7, 5, '=IF(B7=0,0,D7/B7)')
ws0.cell(7, 6, '=B7-D7')
for r in range(4, 8):
    for c in range(1, 7):
        cc = ws0.cell(r, c); cc.border = TB; cc.alignment = CTR
        if r == 7:
            cc.fill = TFILL; cc.font = Font(bold=True, size=14, name='Arial', color='1F2937'); cc.border = TB_TOP
        else:
            cc.fill = Z1 if (r-4) % 2 == 0 else Z2
            cc.font = Font(size=12, name='Arial', color='1F2937')
    ws0.cell(r, 2).number_format = '¥#,##0'
    ws0.cell(r, 4).number_format = '¥#,##0'
    ws0.cell(r, 5).number_format = '0.0%'
    ws0.cell(r, 6).number_format = '¥#,##0'

# 预算表 D4/D5/D6 超链接
for row, sheet in [(4,'硬装'), (5,'主材'), (6,'软装')]:
    cc = ws0.cell(row, 4)
    LNK(cc, f"'{sheet}'!A1")

for col, w in zip('ABCDEFG', [12, 14, 10, 16, 12, 14, 14]):
    ws0.column_dimensions[col].width = w

# --- 三个看板 (row 9 起) ---
# 要求：①标题去掉"分类看板" → 只留"硬装/主材/软装"
#        ②删掉总计行的占比100%列 → 只留类别+金额两列
#        ③标题白字+超链接
WS_START = 9

def build_kanban(start_row, start_col, title_label, categories, sumif_sheet, criteria_col, sum_col, total_ref, jump_map):
    # 标题（白字 + 超链接）
    ws0.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=start_col+1)
    tc = ws0.cell(start_row, start_col, title_label)
    tc.font = Font(bold=True, color='FFFFFF', size=14, name='Arial')
    tc.alignment = LFT
    LNK(tc, f"'{sumif_sheet}'!A1")
    ws0.cell(start_row, start_col).fill = HFILL
    ws0.cell(start_row, start_col+1).fill = HFILL

    # 表头（只留两列：类别 / 金额）
    hr = start_row + 1
    for ci, hname in enumerate(['类别', '金额 (¥)'], 0):
        cc = ws0.cell(hr, start_col + ci, hname)
        cc.font = Font(bold=True, color='FFFFFF', size=12, name='Arial')
        cc.fill = HFILL; cc.alignment = CTR; cc.border = TB

    cur_row = hr + 1
    rows_in_kanban = len(categories)
    for cat_idx, (label, match_val) in enumerate(categories):
        r = cur_row + cat_idx
        # 类别名（超链接，跳到对应分类位置）
        lc = ws0.cell(r, start_col, label)
        if match_val in jump_map:
            js, jref = jump_map[match_val]
            LNK(lc, f"'{js}'!{jref}")
        else:
            LNK(lc, f"'{sumif_sheet}'!A1")
        lc.alignment = LFT; lc.border = TB
        # 金额 SUMIF
        amt = ws0.cell(r, start_col + 1, f'=IFERROR(SUMIF({criteria_col},"{match_val}",{sum_col}),0)')
        amt.number_format = '¥#,##0'; amt.border = TB; amt.alignment = RGT
        fill = Z1 if cat_idx % 2 == 0 else Z2
        for c in range(start_col, start_col + 2):
            ws0.cell(r, c).fill = fill

    # 总计行（只留类别/金额两列，无占比）
    tr = cur_row + rows_in_kanban
    ws0.cell(tr, start_col, '总计').font = Font(bold=True, size=12, name='Arial', color='1F2937')
    ws0.cell(tr, start_col).fill = TFILL
    ws0.cell(tr, start_col).border = TB_TOP
    ws0.cell(tr, start_col).alignment = CTR
    amtt = ws0.cell(tr, start_col + 1, f'={total_ref}')
    amtt.number_format = '¥#,##0'
    amtt.font = Font(bold=True, size=12, name='Arial', color='1F2937')
    amtt.fill = TFILL
    amtt.border = TB_TOP
    amtt.alignment = RGT

    for ci, w in enumerate([18, 16]):
        ws0.column_dimensions[chr(64+start_col+ci)].width = w
    return tr

# 硬装看板
y_cats = [(g, g) for g, _ in y_groups]
y_jumps = {g: ('硬装', f'A{row}') for g, row in group_sub_rows.items()}
build_kanban(WS_START, 1, '硬装', y_cats, '硬装',
             "'硬装'!$A$2:$A$999", "'硬装'!$F$2:$F$999",
             f"'硬装'!$F${y_total}", y_jumps)

# 主材看板
z_cats = [('瓷砖','瓷砖'),('岩板','岩板'),('五金','五金'),('灯具','灯具'),('门','门'),
          ('踢脚线','踢脚线'),('珐琅板','珐琅板'),('洁具','洁具'),('乳胶漆','乳胶漆'),
          ('开关面板','开关面板'),('全屋定制','全屋定制')]
build_kanban(WS_START, 4, '主材', z_cats, '主材',
             "'主材'!$A$2:$A$999", "'主材'!$H$2:$H$999",
             f"'主材'!$H${z_total}",
             {c: ('主材','A1') for _, c in z_cats})

# 软装看板
r_cats = [('电器','电器'),('窗户','窗户'),('暖通','暖通'),('家具','家具'),
          ('床垫','床垫'),('摆件绿植挂画','摆件绿植挂画'),('地毯','地毯'),('窗帘+百叶','窗帘+百叶')]
build_kanban(WS_START, 7, '软装', r_cats, '软装',
             "'软装'!$A$2:$A$999", "'软装'!$G$2:$G$999",
             f"'软装'!$G${r_total}",
             {c: ('软装','A1') for _, c in r_cats})

# 使用说明
note_start = WS_START + 16
ws0.cell(note_start, 1, '💡 使用说明')
ws0.cell(note_start, 1).font = Font(bold=True, size=12, name='Arial', color='1F2937')
ws0.merge_cells(f'A{note_start+1}:G{note_start+7}')
ws0.cell(note_start+1, 1,
    '① 预算表"实际花费"列、三个看板的金额 都是实时 SUMIF 公式，改明细自动刷新\n'
    '② 点击看板标题跳转对应 Sheet；点击类别名跳转该分类的小计行\n'
    '③ 只需改 硬装/主材/软装 三个明细 Sheet，总控自动同步'
)
ws0.cell(note_start+1, 1).font = Font(size=11, name='Arial', color='4B5563')
ws0.cell(note_start+1, 1).alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)

# 先保存成临时文件（此时 hyperlink 还是 openpyxl 写的 External）
tmp_path = '/tmp/budget_tmp.xlsx'
wb.save(tmp_path)
print("✅ 已生成临时文件，正在修 hyperlink XML...")

# ========== 4. 修 XML：把所有 External hyperlink 改成 Internal ==========
# 解压 zip → 替换 hyperlink XML → 删除 rels 中对应的 Relationship → 重新打包
def fix_internal_hyperlinks(xlsx_path, out_path):
    tmpdir = tempfile.mkdtemp()
    with zipfile.ZipFile(xlsx_path, 'r') as zf:
        zf.extractall(tmpdir)

    # 遍历所有 worksheet XML
    sheets_dir = os.path.join(tmpdir, 'xl', 'worksheets')
    fixed_count = 0
    for fname in os.listdir(sheets_dir):
        if not fname.endswith('.xml'): continue
        fpath = os.path.join(sheets_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            xml = f.read()

        # 找出所有 <hyperlink ref="XX" r:id="rIdN"/>
        # 把它们替换成 <hyperlink ref="XX" location="内部地址"/>
        # 同时收集所有用到的 rId
        rids_used = set()
        def replace_hyperlink(m):
            nonlocal fixed_count
            ref = m.group(1)
            rid = m.group(2)
            rids_used.add(rid)
            # 去 rels 文件查 rId 对应的 Target
            # 返回占位符，后面再替换
            fixed_count += 1
            return f'HYPERLINK_PLACEHOLDER_{ref}_{rid}_END'

        xml = re.sub(r'<hyperlink ref="([A-Z]+\d+)" r:id="(rId\d+)"/>', replace_hyperlink, xml)

        if fixed_count > 0:
            # 找对应的 rels 文件
            rels_path = os.path.join(sheets_dir, '_rels', fname + '.rels')
            if os.path.exists(rels_path):
                with open(rels_path, 'r', encoding='utf-8') as f:
                    rels_xml = f.read()
                # 从 rels 里找每个 rId 的 Target
                for rid in rids_used:
                    m2 = re.search(rf'<Relationship[^>]*Id="{rid}"[^>]*Target="([^"]*)"[^>]*/>', rels_xml)
                    if m2:
                        target = m2.group(1)  # 比如 "'硬装'!A5"
                        # 替换占位符为正确的 internal hyperlink XML
                        pattern = f'HYPERLINK_PLACEHOLDER_([A-Z]+\\d+)_{rid}_END'
                        xml = re.sub(pattern, lambda mm: f'<hyperlink ref="{mm.group(1)}" location="{target}"/>', xml)

                # 删掉 rels 文件中用过的 Relationship（因为我们不再用 rId 了）
                # 但保留 rels 文件本身（Excel 可能要求它存在）
                with open(rels_path, 'w', encoding='utf-8') as f:
                    f.write(rels_xml)

                # 删掉 worksheet XML 里的 r: 命名空间声明（如果不再需要）
                # 这个可以忽略，留着不影响

            # 写回 worksheet XML
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(xml)

    # 重新打包
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, tmpdir)
                zf.write(filepath, arcname)

    shutil.rmtree(tmpdir)
    print(f"✅ hyperlink 修复完成，共 {fixed_count} 处 Internal 链接")

out_final = '01-需求与预算/装修控价表-新版.xlsx'
fix_internal_hyperlinks(tmp_path, out_final)
os.remove(tmp_path)
print(f"\n最终文件: {out_final}")
