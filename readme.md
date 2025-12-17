I don't have for byprase for these state so it can do in localy if are you in india

Rajasthan
Assam
Chhattisgarh
MadhyaPradesh
Andhrapradesh
Karnataka

Rajasthan:
curl -X POST "https://diprfrontwebapi.rajasthan.gov.in//api/JankalyanHome/GetAchievementListBySearchFilter?isRequiredAttachImages=true" \
-H "Content-Type: application/json" \
-H "User-Agent: Mozilla/5.0" \
-H "Origin: https://dipr.rajasthan.gov.in" \
-H "Referer: https://dipr.rajasthan.gov.in/" \
-H "x-api-key: UvpJvSho3uMrjwJeOWpU+MZRydSjdsiJc6MhmSu0PyMvngXe+lYwv/3DTawSJ/zf" \
-d '{
"AdmDepartmentCode": 0,
"DepartmentCode": 85,
"CategoryCode": 8,
"SubCategoryCode": 0,
"FromDate": "",
"ToDate": "",
"IndexModel": {
"AdvanceSearchModel": {
"SearchKeyword": "",
"RadioStateDistrict": [
{"Disabled":false,"Group":null,"Selected":false,"Text":"Department Level","Value":"30206"},
{"Disabled":false,"Group":null,"Selected":false,"Text":"District Level","Value":"30205"},
{"Disabled":false,"Group":null,"Selected":false,"Text":"State Level","Value":"30204"}
],
"ddlAllDepartmentAsDistrict": [
{"OtherData":{"DepartmentTitleHindi":"जिला अजमेर","AdminDepartmentCode":11},"Disabled":false,"Group":null,"Selected":false,"Text":"Ajmer","Value":"1"}
]
},
"PageSize": 10,
"IsPostBack": false,
"OrderByAsc": 0,
"Search": null,
"OrderBy": "PressreleaseDate",
"Page": 1
},
"IsActive": 1
}'

old
