
# drfRBAC
<font color=#999AAA >基于Django REST framework的 **接口级别权限** 角色访问控制
- 自动权限类生成
- 自动权限表数据生成
- 自动权限校验
- 只需着重于权限的分配
<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

<br/>

# 前言
## 1. drf7表
- **User** - 用户表 
- **Role** - 角色表 （可作为岗位）
- **Group** - 分组表 （可作为部门）
- **Permissions** - 权限表
- **UserRole** - 用户角色多对多中间表
- **UserPermissions** - 用户权限多对多中间表
- **RolePermissions** - 角色权限多对多中间表
- 表关联关系如下：

![数据表关系](https://img-blog.csdnimg.cn/20210312175503638.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1dSaGFu,size_16,color_FFFFFF,t_70#pic_center)
> 使用 **db_constraint=False** 无物理外键

<br/>

## 2. 鸭子角色
> “ 如果一个角色有些像鸭子、且有和鸭子一样游泳的权限、和鸭子一样叫的权限、和鸭子一样的所有权限，那么这个角色就是鸭子。”
- **角色**（role）在访问控制逻辑中**不参与**任何逻辑判断，只作为有**同类权限**用户的合集，方便同角色用户的**权限继承** <br/> <br/>
	- > e.g.  <br/>
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;客服**角色**拥有<访问**查看客户**接口>的权限 <br/>
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;那么所有**角色为客服的用户** 就都继承有<访问**查看客户**接口>的权限 <br/>
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;如果**用户**本身拥有<访问**查看客户**接口>的权限，那么当前用户在访问控制逻辑中就可以**视为客服** <br/>
- \* 只适用于 **访问控制逻辑** 不适用于 **业务逻辑**， 如接口内容为查看 **角色为客服的所有用户** ，则无法获取到 **拥有与客服完全相同权限** 用户的数据
- **用户**（user）可通过计算属性 **get_permissions** 来获取由**自己的权限** （UserRole）  和**继承自角色（identity）的权限** （RolePermissions） 组成的列表

<br/>

## 3. 权限核心
> \* 进行访问控制前需进行 **用户认证**，详见 Module_Auth.Authentications.RBAC_Authentications => DEMO
- 所有接口 如果需要进行访问控制，**都可以 / 应该** 进行权限判断 （权限类可使用新的 **action装饰器** 快速**创建**，并自动**生成**对应数据，**无需**反复手动创建drf权限类）
- 权限为访问控制的**唯一核心**，无论什么身份，只要用户拥有接口所需的权限，即可访问该接口，否则**访问会被拦截**


<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">
<br/>

# 一、快速使用
## 1. 依赖/包
- django 2.2
- MySQL 8
- Django REST framework
- pymsql

<br/>

## 2. 准备
### 2.1. 创建key文件
- 在 **Module_Key** 下创建 **key.py** 文件 内容如下：
```python
# 修改token盐 数据库链接信息 抽离 settings.secret_key,settings.allowed_hosts
RBAC_token_salt = ""

project_database = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "3306"
    }
}
project_secret_key = ''
project_allowed_hosts = []
```
<br/>

### 2.2. 数据库同步
- migrate并运行项目
- permissions表会 **自动生成** 13条权限数据（除管理员权限外，其余12条来自**DEMO** 详见TODO注释，可方便定位DEMO位置）

|...|name|codeName|
|--|--|--|
|...  |管理员权限|AdminPermission|
|...  |获取全部用户信息|GET_UserPermission|
|...  |修改全部用户信息|PUT_UserPermission|
|...  |创建全部用户信息|POST_UserPermission|
|...  |删除全部用户信息|DELETE_UserPermission|
|...  |获取特定分组下用户信息|GET_GroupUserPermission|
|...  |修改特定分组下用户信息|PUT_GroupUserPermission|
|...  |创建特定分组下用户信息|POST_GroupUserPermission|
|...  |删除特定分组下用户信息|DELETE_GroupUserPermission|
|...  |获取指定角色用户|GET_role_user|
|...  |修改指定角色用户|PUT_role_user|
|...  |创建指定角色用户|POST_role_user|
|...  |删除指定角色用户|DELETE_role_user|


<br/>

### 2.3. 测试使用
- 数据库创建 **测试用户** 数据
- 为测试用户分配权限 （**UserPermissions** 表）
- 使用 `/v1/RBAC/Login/` 接口获取 **token**  👇

![登录请求](https://img-blog.csdnimg.cn/20210315173807517.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1dSaGFu,size_16,color_FFFFFF,t_70#pic_center)
- 请求头中 **携带token** 即可访问DEMO中提供的路由（需要拥有对应权限，否则会被拦截） 👇

![token](https://img-blog.csdnimg.cn/20210315173833181.jpg#pic_center)
- DEMO提供 **3个** 案例路由，对应所需权限如下表（每个路由对应 **增删改查** 四种权限）：

<table>
  <thead>
    <tr>
      <th>url</th>
      <th>name</th>
      <th>codeName</th>
    </tr>
  </thead>
  <tbody>
    <tr bgcolor="#EFF3F5">
      <td rowspan="4">/v1/RBAC/user/</td>
      <td>获取全部用户信息</td>
      <td>GET_UserPermission</td>
    </tr>
    <tr>
      <td>修改全部用户信息</td>
      <td>PUT_UserPermission</td>
    </tr>
    <tr>
      <td>创建全部用户信息</td>
      <td>POST_UserPermission</td>
    </tr>
    <tr>
      <td>删除全部用户信息</td>
      <td>DELETE_UserPermission</td>
    </tr>
    <tr bgcolor="#EFF3F5">
      <td rowspan="4">/v1/RBAC/user/group_user/</td>
      <td>获取特定分组下用户信息</td>
      <td>GET_GroupUserPermission</td>
    </tr>
    <tr>
      <td>修改特定分组下用户信息</td>
      <td>PUT_GroupUserPermission</td>
    </tr>
    <tr>
      <td>创建特定分组下用户信息</td>
      <td>POST_GroupUserPermission</td>
    </tr>
    <tr>
      <td>删除特定分组下用户信息</td>
      <td>DELETE_GroupUserPermission</td>
    </tr>
    <tr bgcolor="#EFF3F5">
      <td rowspan="4">/v1/RBAC/user/role_user/</td>
      <td>获取指定角色用户</td>
      <td>GET_role_user</td>
    </tr>
    <tr>
      <td>修改指定角色用户</td>
      <td>PUT_role_user</td>
    </tr>
    <tr>
      <td>创建指定角色用户</td>
      <td>POST_role_user</td>
    </tr>
    <tr>
      <td>删除指定角色用户</td>
      <td>DELETE_role_user</td>
    </tr>
  </tbody>
</table>

- 为用户分配某一权限，该用户即可用此权限对应的 **请求方式** 访问该权限对应的 **接口**
- > e.g.  <br/>
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;角色**拥有** <获取全部用户信息GET_UserPermission> 权限时 ，即可对 **/v1/RBAC/user/** 接口进行 **GET** 请求<br/>
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;角色**没有** <创建指定角色用户POST_role_user> 权限时 ，若对 **/v1/RBAC/user/role_user/** 接口进行 **PUT** 请求，则会被**拦截**<br/>

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">
<br/>

# 二、推荐的路由层级标准
 > **示例1**：www.wrhan.cn/v1/RBAC/**user**/ <br/>
 > **示例2**：www.wrhan.cn/v1/RBAC/**user**/**role_user**/ <br/>
 > **示例3**：www.wrhan.cn/v1/RBAC/**group_user**/**role_user**/ <br/>

- 路由对应的 **含义** 👇：
 > **示例1**：域名/版本号/模块名/**所有用户**/ <br/>
 > **示例2**：域名/版本号/模块名/**所有用户**/**指定为某一种角色的用户**/ <br/>
 > **示例3**：域名/版本号/模块名/**某一分组的所有用户**/**指定为某一种角色的用户**/ <br/>

- 路由对应的 **数据** 👇：
 > **示例1**：域名/版本号/模块名/针对**某张表**的数据/ <br/>
 > **示例2**：域名/版本号/模块名/针对**某张表**的数据/此表数据中的**细分数据**/ <br/>
 > **示例3**：域名/版本号/模块名/针对某张表**某个顶级分类**的数据/此分类数据中的**细分数据**/ <br/>

- 路由对应的 **生成** 👇：
 > **示例1**：域名/版本号/模块名/**基于ModelViewSet的自动路由**/ <br/>
 > **示例2**：域名/版本号/模块名/**基于ModelViewSet的自动路由**/**action生成的自动路由**/ <br/>
 > **示例3**：域名/版本号/模块名/**基于ModelViewSet的自动路由**/**action生成的自动路由**/ <br/>

- 路由对应的 **权限** 👇：
 > **示例1**：域名/版本号/模块名/**一级权限**/ <br/>
 > **示例2**：域名/版本号/模块名/**一级权限**/**二级权限**/ <br/>
 > **示例3**：域名/版本号/模块名/**一级权限**/**二级权限**/ <br/>

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">
<br/>
