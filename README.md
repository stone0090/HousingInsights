# HousingInsights

- 手动登录kb网站获取Cookie，填充到fetch_bk_deals.py的main函数中
- 执行fetch_bk_deals.py的main函数，获取bk最近3000天成交数据储存为json
- 执行csv_util.py的main函数，把json文件转为csv文件
- 然后自己搭一个mysql数据库，把csv数据导入mysql数据库进行分析

```sql
CREATE DATABASE bk_deals CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 导入csv数据
create table `history3000_2024-01-13`
(
    xiaoqu         varchar(100) null,
    fangxing       varchar(100) null,
    mianji         double       null,
    chaoxiang      varchar(100) null,
    zhuangxiu      varchar(100) null,
    dealDate       varchar(100) null,
    totalPrice     double       null,
    unitPrice      double       null,
    positionInfo   varchar(100) null,
    dealHouseInfo  varchar(100) null,
    dealCycleeInfo varchar(100) null,
    district       varchar(100) null
);
    
insert into `history3000_2024-01-13` (xiaoqu,fangxing,mianji,chaoxiang,zhuangxiu,dealDate,totalPrice,unitPrice,positionInfo,dealHouseInfo,dealCycleeInfo,district)
select * from `history3000_haizhu_2024-01-13`;

insert into `history3000_2024-01-13` (xiaoqu,fangxing,mianji,chaoxiang,zhuangxiu,dealDate,totalPrice,unitPrice,positionInfo,dealHouseInfo,dealCycleeInfo,district)
select * from `history3000_liwan_2024-01-13`;

insert into `history3000_2024-01-13` (xiaoqu,fangxing,mianji,chaoxiang,zhuangxiu,dealDate,totalPrice,unitPrice,positionInfo,dealHouseInfo,dealCycleeInfo,district)
select * from `history3000_tianhe_2024-01-13`;

insert into `history3000_2024-01-13` (xiaoqu,fangxing,mianji,chaoxiang,zhuangxiu,dealDate,totalPrice,unitPrice,positionInfo,dealHouseInfo,dealCycleeInfo,district)
select * from `history3000_yuexiu_2024-01-13`;

```