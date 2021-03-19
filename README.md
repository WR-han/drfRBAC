# <a id="drfRBAC">drfRBAC</a>

<font color=#999AAA >基于Django REST framework的 **接口级别权限** 角色访问控制

- **自动权限类生成**
- **自动权限表数据生成**
- **自动权限校验**
- **只需着重于权限的分配**
<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

# 目录

- [前言](#前言)
	- [1.&nbsp;drf7表](#drf7表)
	- [2.&nbsp;鸭子角色](#鸭子角色)
	- [3.&nbsp;用户认证（authentication）](#用户认证（authentication）)
	- [4.&nbsp;接口级别权限](#接口级别权限)
	- [5.&nbsp;权限自动验证机制](#权限自动验证机制)
- [一、快速使用](#一、快速使用)
	- [1.&nbsp;依赖/包](#包)
	- [2.&nbsp;准备](#准备)
		- [2.1.&nbsp;创建key文件](#创建key文件)
		- [2.2.&nbsp;数据库同步](#数据库同步)
		- [2.3.&nbsp;使用](#使用)
- [二、推荐的路由层级](#二、推荐的路由层级)
- [三、权限详解](#三、权限详解)
	- [1.&nbsp;基础权限类](#基础权限类)
	- [2.&nbsp;自定义权限类（主要使用）](#自定义权限类（主要使用）)
		- [2.1&nbsp;一级权限类](#一级权限类)
		- [2.2&nbsp;二级权限类](#二级权限类)
			- [2.2.1&nbsp;普通二级权限类](#普通二级权限类)
			- [2.2.2&nbsp;通用二级权限类（常用）](#通用二级权限类（常用）)
			- [2.2.3&nbsp;普通&nbsp;/&nbsp;通用二级权限类的选择](#通用二级权限类的选择)
		- [2.3&nbsp;一&nbsp;/&nbsp;二级权限类的使用关系](#二级权限类的使用关系)
	- [3.&nbsp;权限表数据生成](#权限表数据生成)
		- [3.1&nbsp;生成数量与主要字段](#生成数量与主要字段)
		- [3.2&nbsp;自动生成方式](#自动生成方式)
			- [3.2.1&nbsp;手动创建权限类（一级权限类&nbsp;/&nbsp;普通二级权限类）的权限数据生成方式](#普通二级权限类）的权限数据生成方式)
      - [3.2.2&nbsp;自动创建权限类（通用二级权限类）的权限数据生成方式](#自动创建权限类（通用二级权限类）的权限数据生成方式)
	- [4.&nbsp;新action装饰器（主要使用）](#新action装饰器（主要使用）)
		- [4.1&nbsp;permission参数](#permission参数)
		- [4.2&nbsp;inherit参数](#inherit参数)
<br/>

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

<br/>

# <a id="前言">前言</a>
## <a id="drf7表">1. drf7表</a>
- **User** - 用户表 
- **Role** - 角色表 （可作为岗位）
- **Group** - 分组表 （可作为部门）
- **Permissions** - 权限表
- **UserRole** - 用户角色多对多中间表
- **UserPermissions** - 用户权限多对多中间表
- **RolePermissions** - 角色权限多对多中间表
- 表关联关系如下：

![数据表关系](https://img-blog.csdnimg.cn/20210319155812248.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1dSaGFu,size_16,color_FFFFFF,t_70#pic_center)
> 使用 **db_constraint=False** 无物理外键

<br/>

## <a id="鸭子角色">2. 鸭子角色</a>
> “ 如果一个角色有些像鸭子、且有和鸭子一样游泳的权限、和鸭子一样叫的权限、和鸭子一样的所有权限，那么这个角色就是鸭子。”
- **角色**（Role）在访问控制逻辑中**不参与**任何逻辑判断，只作为有**同类权限**用户的合集，方便同角色用户的**权限继承** <br/> <br/>
	- > e.g.  <br/>
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;客服**角色**拥有<访问**查看客户**接口>的权限 <br/>
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;那么所有**角色为客服的用户** 就都继承有<访问**查看客户**接口>的权限 <br/>
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;如果**用户**本身拥有<访问**查看客户**接口>的权限，那么当前用户在访问控制逻辑中就可以**视为客服** <br/>
- 只适用于 **访问控制逻辑** 不适用于 **业务逻辑**， 如接口内容为查看 **角色为客服的所有用户** ，则无法获取到 **拥有与客服完全相同权限** 用户的数据
- **权限**（Permission）为访问控制的 **唯一核心** ，无论什么身份，只要用户拥有接口所需的权限，即可访问该接口，否则 **访问会被拦截**
- **用户**（User）可通过计算属性 **get_permissions** 来获取由**自己的权限** （UserRole）  和**继承自角色**（Role）**的权限** （RolePermissions） 组成的列表

<br/>

## <a id="用户认证（authentication）">3. 用户认证（authentication）</a>
> - \* 进行访问控制前 **必须** 进行 **用户认证**，案例详见 `Module_Auth.Authentications.RBAC_Authentications` => DEMO  <br/>
> - 使用 **drf原生authentication** ，用法不过多赘述，若不进行用户认证，则 **无法** 进行 **权限自动验证**

<br/>

## <a id="接口级别权限">4. 接口级别权限</a>
- 所有 **接口** 如果需要进行访问控制，**都可以 / 应该** 进行权限判断 （权限类可使用 **新的action装饰器** 快速**创建**，并自动**生成**对应数据，**无需** 反复手动创建drf权限类）

<br/>

## <a id="权限自动验证机制">5. 权限自动验证机制</a>
1. 当接口 **手动** / **自动** 配置 **权限类** 后，便会在 **Permission表** 中 **自动生成** 对应该接口的 **4条** 权限数据 （分别为允许 **GET/PUT/POST/DELETE** 四种方式请求此接口的权限）
2. 当用户访问此接口时（已通过drf的 **authentication** 验证的前提下），若该用户拥有 **1.中生成** 且与当前 **请求方式对应** 的权限（**UserPermissions表**），则可以访问该接口，否则 **访问会被拦截**
<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">
<br/>

# <a id="一、快速使用">一、快速使用</a>
## <a id="包">1. 依赖/包</a>
- django 2.2
- MySQL 8
- Django REST framework
- pymsql
- PyJWT

<br/>

## <a id="准备">2. 准备</a>
### <a id="创建key文件">2.1. 创建key文件</a>
- 在 `Module_Key` 下创建 `key.py` 文件 内容如下：
```python
""" 修改token盐 数据库链接信息 抽离 settings.secret_key,settings.allowed_hosts """
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

### <a id="数据库同步">2.2. 数据库同步</a>
- migrate并运行项目
- permissions表会 **自动生成** 10条权限数据（除 **管理员权限** 外，其余9条来自**DEMO**，详见代码 **TODO** 注释，可方便定位DEMO位置）

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

<br/>

### <a id="使用">2.3. 使用</a>
- 数据库创建 **测试用户** 数据
- 为测试用户分配权限 （**UserPermissions** 表）
- 使用 `/v1/RBAC/Login/` 接口获取 **token**  👇

![登录请求](https://img-blog.csdnimg.cn/20210315173807517.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1dSaGFu,size_16,color_FFFFFF,t_70#pic_center)
- 请求头中 **携带token** 即可访问DEMO中提供的路由（需要拥有对应权限，否则会被拦截） 👇

![token](https://img-blog.csdnimg.cn/20210315173833181.jpg#pic_center)
- DEMO提供 **3个** 案例路由，对应所需权限如下表（具体请查看 **[👇3. 权限表数据生成](#权限表数据生成)** ）：

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
  </tbody>
</table>

- 为用户分配某一权限，该用户即可用此权限对应的 **请求方式** 访问该权限对应的 **接口**
- > e.g.  <br/>
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;角色**拥有** <获取全部用户信息GET_UserPermission> 权限时 ，即可对 **/v1/RBAC/user/** 接口进行 **GET** 请求<br/>
	 	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;角色**没有** <创建特定分组下用户信息POST_GroupUserPermission> 权限时 ，若对 **/v1/RBAC/user/group_user/** 接口进行 **POST** 请求，则会被**拦截**<br/>
	 

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">
<br/>

# <a id="二、推荐的路由层级">二、推荐的路由层级</a>
 > **示例1**：.../v1/RBAC/**user**/ <br/>
 > **示例2**：.../v1/RBAC/**user**/**role_user**/ <br/>
 > **示例3**：.../v1/RBAC/**group_user**/**role_user**/ <br/>

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

# <a id="三、权限详解">三、权限详解</a>
## <a id="基础权限类">1. 基础权限类</a>
> 基础权限类分为两种，均继承自 drf **BasePermission**类， **仅供** 自定义权限类 **继承使用**
- **MainPermission**
	-  **位置**：`Module_Custom.Custom_Permission` => MainPermission
- **SecondaryPermission**
	-  **位置**：`Module_Custom.Custom_Permission` => SecondaryPermission

<br/>

## <a id="自定义权限类（主要使用）">2. 自定义权限类（主要使用）</a>
> 请配置于 `Module_Auth.Permissions` 中（其中已有**DEMO** `RBAC_Permissions.py`）<br/>
> 权限类 **必须要写** 注释 具体原因请查看 **[👇3. 权限表数据生成](#权限表数据生成)** <br/>
> `Module_Auth.Permissions` 下所有模块中的类，都会在 **Permissions表** 中自动生成权限数据 <br/>
> - 具体生成格式请查看 **[👇3. 权限表数据生成](#权限表数据生成)** 
> - 请确保 `Module_Auth.Permissions` 下所有模块中的类，都继承自基础权限类（**MainPermission** /**SecondaryPermission** ），以免产生**无效**权限表数据

<br/>

### <a id="一级权限类">2.1 一级权限类</a>
> 所有继承自 **MainPermission类** 的权限类皆为 **一级权限类**
- **创建方法**
	- 直接继承 **MainPermission类** ，如无需重写drf权限类的 **has_permission** 方法，内部直接 **pass** 即可
	- **必须要写注**释 ，注释内容为此权限的 **释义** ，用作权限数据生成，具体请查看 **[👇3. 权限表数据生成](#权限表数据生成)** 
```python
class UserPermission(MainPermission):
    """
    全部用户信息
    """
    ...
```

- **使用方法**
	- 一级权限类与drf原有权限类使用方法相同，配置于 **permission_classes** 之中
	- 一级权限往往表示对 **整个视图集所有自动路由接口** 的权限控制
```python
class Users(ModelViewSet):

    # 一级权限认证 ↓
    permission_classes = [UserPermission]

    authentication_classes = [UserAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

<br/>

### <a id="二级权限类">2.2 二级权限类</a>
> 所有继承自 **SecondaryPermission类** 的权限类皆为 **二级权限类**

<br/>

#### <a id="普通二级权限类">2.2.1 普通二级权限类</a>
- **创建方法**
	- 直接继承 **SecondaryPermission类** ，如无需重写drf权限类的 **has_permission** 方法，内部直接 **pass** 即可
	- 必须要写 **注释** ，注释内容为此权限的 **释义** ，用作权限数据生成，具体请查看 **[👇3. 权限表数据生成](#权限表数据生成)** 
```python
class GroupUserPermission(SecondaryPermission):
    """
    特定分组下用户信息
    """
    ...
```
- **使用方法**
	- 普通二级权限类 **不能** 配置于 **permission_classes** 之中
	- 普通二级权限类需配置于 **新action装饰器** 的 **permission参数** 中，具体请查看 **[👇4. 新action装饰器](#新action装饰器（主要使用）)** 
	- 二级权限往往表示对 视图集中某个**action自动路由接口** 的权限控制
```python
    @action(methods=["get"], detail=False, permission=GroupUserPermission, inherit=False)
    def group_user(self, request):
        return Response({
            "code": 200
        })
```

<br/>

#### <a id="通用二级权限类（常用）">2.2.2 通用二级权限类（常用）</a>
- **无需手动创建**
- **使用方法**
	- 以 **字符串类型** 实参传入 **新action装饰器** 的 **permission参数** 中即可，此参数作为该权限的 **释义**
		- **新action装饰器** 会在内部自动生成一个 **通用二级权限类** 并进行配置
		- 此 **通用二级权限类** 的类名为 **被装饰方法** 的**方法名** 
```python
    @action(methods=["get"], detail=False, permission="指定角色用户", inherit=True)
    def role_user(self, request):
        return Response({
            "code": 200
        })
```
**👆上述DEMO** 会自动生成一个**通用二级权限类**，其功能 / 自动生成的权限表数据，**和下述👇** 普通二级权限类 **相同**

```python
"""伪代码"""
class role_user(SecondaryPermission):
    """
    指定角色用户
    """
    ...
```

<br/>

#### <a id="通用二级权限类的选择">2.2.3 普通 / 通用二级权限类的选择</a>
> **通常情况** 下使用 **通用二级权限类** 即可，更加方便快捷，只需在action装饰器中传入 **释义字符串**，无需手动创建权限类

- 而以下情况则需要 **手动创建** 普通二级权限类：
	-  需要重写权限类的 **has_permission** 方法
	- **多个二级权限接口** 需使用 **同一个**二级权限 （**多个action装饰器** 的permission参数传入 **同一个** 普通二级权限类）
		- 👆此类需求较为常见

<br/>

### <a id="二级权限类的使用关系">2.3 一 / 二级权限类的使用关系</a>
> 一 / 二级权限类皆可 **单独使用** （只配置一级权限或二级权限）<br/>
> 同时使用时的验证先后顺序请查看 **👇[4.2 inherit参数](#inherit参数)**

<br/>

## <a id="权限表数据生成">3. 权限表数据生成</a>

<br/>

### <a id="生成数量与主要字段">3.1 生成数量与主要字段</a>
> 每一个权限类，会自动生成 **四条** 权限数据，分别对应四种请求方式 如 **UserPermission** 权限会生成以下四种权限数据（具体请查看 **[👇3.2 自动生成方式](#自动生成方式)**）
- **GET:** GET_UserPermission
- **PUT：** PUT_UserPermission
- **POST：** POST_UserPermission
- **DELETE：** DELETE_UserPermission

> 权限表数据拥有两个主要字段：**name**、**codeName**
- **name:** 权限的名称，即 **释义**
- **codeName：** 权限的代码，往往由 **请求方式_权限类名** 组成，供 **权限验证** 时使用

<br/>

### <a id="自动生成方式">3.2 自动生成方式</a>
> 自动生成来源有两种：<br/>
> - 手动创建于 `Module_Auth.Permissions` 中的权限类，包括 **一级权限类** 和 **普通二级权限类** <br/>
> - **新action装饰器** 中自动生成的通用二级权限类<br/>

<br/>

#### <a id="普通二级权限类）的权限数据生成方式">3.2.1 手动创建权限类（一级权限类 / 普通二级权限类）的权限数据生成方式</a>
- 表字段来源如下：
	- name => `f"{请求方式对应的中文}{当前类的注释内容}"`
	- codeName => `f"{请求方式}_{当前类名}"`

```python
class UserPermission(MainPermission):
    """
    全部用户信息
    """
    ...
```

- 生成的Permissions表数据：

|name|codeName|
|--|--|
|获取全部用户信息|GET_UserPermission|
|修改全部用户信息|PUT_UserPermission|
|创建全部用户信息|POST_UserPermission|
|删除全部用户信息|DELETE_UserPermission|

- 源码位置 `APPS.RBAC.apps`

<br/>

#### <a id="自动创建权限类（通用二级权限类）的权限数据生成方式">3.2.2 自动创建权限类（通用二级权限类）的权限数据生成方式</a>
- 表字段来源如下：
	- name => `f"{请求方式对应的中文}{新action装饰器permission参数中的 字符串}"`
	- codeName => `f"{请求方式}_{被新action装饰器所装饰方法的 方法名 }"`
- 生成权限数据数量：
	- 和 **手动创建权限类** 生成数据不同，通用二级权限类 **只会生成** 新action装饰器中 **methods参数** 允许请求方式 **所对应的** 权限数据

```python
@action(methods=["get"], detail=False, permission="指定角色用户", inherit=True)
def role_user(self, request):
    return Response({
        "code": 200
    })
```
- 生成的Permissions表数据：

|name|codeName|
|--|--|
|获取指定角色用户|GET_role_user|

- 源码位置 `Module_Custom.Custom_Permission.action`

<br/>

## <a id="新action装饰器（主要使用）">4. 新action装饰器（主要使用）</a>
> 内置二级权限认证，新增两个参数：**permission** 和 **inherit**

<br/>

### <a id="permission参数">4.1 permission参数</a>
> 是否需要进行二级权限认证

- 参数类型：**二级权限类**（class） / **释义** （str）
	- 当参数为 **二级权限类** 时，直接进行权限验证
	- 当参数为 **释义** 时，会先根据释义自动生成通用 **二级权限类** ，再进行权限验证
- 参数默认值：**None**

<br/>

### <a id="inherit参数">4.2 inherit参数</a>
> 是否继承一级权限（permission_classes中的权限类）的 **认证结果**

- 参数类型：**bool**
	- 当参数为 **True** 时，表示继承  （等同于一二级权 **限验证结果** 的 **或** 关系）：
		- 若 **一级权限通过** 则 **无需进行** 二级权限验证
		- 若 **一级权限未通过** 或 **没有设置一级权限** 时， **再进行** 二级权限验证
	- 当参数为 **Fales** 时，表示不继承：
		- 无论 **一级权限是否通过** ，只以  **二级权限验证结果** 为准
- 参数默认值：**True**
