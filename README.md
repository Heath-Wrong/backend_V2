## [#](#声纹识别-api-文档) 声纹识别 API 文档

## [#](#接口说明) 接口说明

声纹识别（Voiceprint Recognition），是一项提取说话人声音特征和说话内容信息，自动核验说话人身份的技术。可以将说话人声纹信息与库中的已知用户声纹进行1:1比对验证和1:N的检索，当声纹匹配时即为验证/检索成功。  
**温馨提示：声纹识别服务已升级，请新老用户尽快切换到此WebAPI接口，感谢理解与支持！**

调用过程中涉及步骤如下：  
**1、创建声纹特征库（必须）  
**2、添加音频特征（必须）  
**3、特征比对1:1（必须）  
**4、特征比对1:N（必须）  
**5、查询特征列表（非必须）  
6、更新音频特征（非必须）  
7、删除指定特征（非必须）  
8、删除声纹特征库（非必须）

## [#](#接口demo) 接口Demo

**示例demo**请点击 **[这里](#%E8%B0%83%E7%94%A8%E7%A4%BA%E4%BE%8B)** 下载。  
demo 覆盖部分语言，其他语言参照下方接口文档进行开发。  
欢迎热心的开发者到[讯飞开放平台社区 (opens new window)](http://bbs.xfyun.cn/)分享你们的demo。  

## [#](#接口要求) 接口要求

集成声纹识别API时，需按照以下要求。

| 内容 | 说明 |
| --- | --- |
| 传输方式 | http\[s\] (为提高安全性，强烈推荐https) |
| 请求地址 | http\[s\]: //api.xf-yun.com/v1/private/s782b4996  
*注：服务器IP不固定，为保证您的接口稳定，请勿通过指定IP的方式调用接口，使用域名方式调用* |
| 请求行 | POST /v1/private/s782b4996 HTTP/1.1 |
| 接口鉴权 | 签名机制，详情请参照下方[鉴权认证](#%E9%89%B4%E6%9D%83%E8%AE%A4%E8%AF%81) |
| 字符编码 | UTF-8 |
| 响应格式 | 统一采用JSON格式 |
| 开发语言 | 任意，只要可以向讯飞云服务发起HTTP请求的均可 |
| 适用范围 | 任意操作系统，但因不支持跨域不适用于浏览器 |
| 音频格式 | 采样率16k、位长16bit、单声道的mp3 |
| 音频大小 | base64编码后大小不超过4M，音频内容请尽量保持清晰，且有效帧大于0.5s（建议使用3-5秒的音频） |

## [#](#接口调用流程) 接口调用流程

• 通过接口密钥基于hmac-sha256计算签名，将签名以及其他参数加在请求地址后面。详见下方 [鉴权认证](#%E9%89%B4%E6%9D%83%E8%AE%A4%E8%AF%81) 。  
• 将请求参数以及图片数据放在Http Request Body中，以POST表单的形式提交，详见下方 [请求参数](#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0) 。  
• 向服务器端发送Http请求后，接收服务器端的返回结果。  

### [#](#鉴权认证) 鉴权认证

在调用业务接口时，请求方需要对请求进行签名，服务端通过签名来校验请求的合法性。

#### [#](#鉴权方法) 鉴权方法

通过在请求地址后面加上鉴权相关参数的方式，**请注意影响鉴权结果的值有url、APISecret、APIKey、date，如果调试鉴权，请务必按照示例中给的值进行调试**，具体参数如下：

http示例url：

```text
https://api.xf-yun.com/v1/private/s782b4996?authorization=YXBpX2tleT0iYXBpa2V5WFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFgiLCBhbGdvcml0aG09ImhtYWMtc2hhMjU2IiwgaGVhZGVycz0iaG9zdCBkYXRlIHJlcXVlc3QtbGluZSIsIHNpZ25hdHVyZT0iMWp3UWJJQUttUUU3SndJSDBJRHhpQzFwZWpybE4rVnBIWERXT0ZWeTVOTT0i&host=api.xf-yun.com&date=Fri%2C+23+Apr+2021+02%3A35%3A47+GMT
```

鉴权参数：

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| host | string | 是 | 请求主机 | api.xf-yun.com |
| date | string | 是 | 当前时间戳，RFC1123格式("EEE, dd MMM yyyy HH:mm:ss z") | Fri, 23 Apr 2021 02:35:47 GMT |
| authorization | string | 是 | 使用base64编码的签名相关信息(签名基于hamc-sha256计算) | 参考下方详细生成规则 |

• date参数生成规则：

date必须是UTC+0或GMT时区，RFC1123格式(Fri, 23 Apr 2021 02:35:47 GMT)。  
服务端会对date进行时钟偏移检查，最大允许300秒的偏差，超出偏差的请求都将被拒绝。

• authorization参数生成格式：

1）获取接口密钥APIKey 和 APISecret。  
在讯飞开放平台控制台，创建一个应用后即可获取，均为32位字符串。  
2）参数authorization base64编码前（authorization\_origin）的格式如下。  

```text
api_key="$api_key",algorithm="hmac-sha256",headers="host date request-line",signature="$signature"
```

其中 api\_key 是在控制台获取的APIKey，algorithm 是加密算法（仅支持hmac-sha256），headers 是参与签名的参数（见下方注释）。  
signature 是使用加密算法对参与签名的参数签名后并使用base64编码的字符串，详见下方。

***注：* headers是参与签名的参数，请注意是固定的参数名（"host date request-line"），而非这些参数的值。**

3）signature的原始字段(signature\_origin)规则如下。  

signature原始字段由 host，date，request-line三个参数按照格式拼接成，  
拼接的格式为(\\n为换行符,’:’后面有一个空格)：

```text
host: $host\ndate: $date\n$request-line
```

假设

```text
请求url = "https://api.xf-yun.com/v1/private/s782b4996"
date = "Fri, 23 Apr 2021 02:35:47 GMT"
```

那么 signature原始字段(signature\_origin)则为：

```text
host: api.xf-yun.com
date: Fri, 23 Apr 2021 02:35:47 GMT
POST /v1/private/s782b4996 HTTP/1.1
```

4）使用hmac-sha256算法结合apiSecret对signature\_origin签名，获得签名后的摘要signature\_sha。  

```text
signature_sha=hmac-sha256(signature_origin,$apiSecret)
```

其中 apiSecret 是在控制台获取的APISecret  

5）使用base64编码对signature\_sha进行编码获得最终的signature。

```text
signature=base64(signature_sha)
```

假设

```text
APISecret = "apisecretXXXXXXXXXXXXXXXXXXXXXXX"	
date = "Fri, 23 Apr 2021 02:35:47 GMT"
```

则signature为

```text
signature="1jwQbIAKmQE7JwIH0IDxiC1pejrlN+VpHXDWOFVy5NM="
```

6）根据以上信息拼接authorization base64编码前（authorization\_origin）的字符串，示例如下。  

```text
api_key="apikeyXXXXXXXXXXXXXXXXXXXXXXXXXX", algorithm="hmac-sha256", headers="host date request-line", signature="1jwQbIAKmQE7JwIH0IDxiC1pejrlN+VpHXDWOFVy5NM="
```

*注：* headers是参与签名的参数，请注意是固定的参数名（"host date request-line"），而非这些参数的值。  

7）最后再对authorization\_origin进行base64编码获得最终的authorization参数。

```text
authorization = base64(authorization_origin)
示例结果为：
authorization=YXBpX2tleT0iYXBpa2V5WFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFgiLCBhbGdvcml0aG09ImhtYWMtc2hhMjU2IiwgaGVhZGVycz0iaG9zdCBkYXRlIHJlcXVlc3QtbGluZSIsIHNpZ25hdHVyZT0iMWp3UWJJQUttUUU3SndJSDBJRHhpQzFwZWpybE4rVnBIWERXT0ZWeTVOTT0i
```

#### [#](#鉴权结果) 鉴权结果

如果鉴权失败，则根据不同错误类型返回不同HTTP Code状态码，同时携带错误描述信息，详细错误说明如下：

| HTTP Code | 说明 | 错误描述信息 | 解决方法 |
| --- | --- | --- | --- |
| 401 | 缺少authorization参数 | {"message":"Unauthorized"} | 检查是否有authorization参数，详情见[authorization参数详细生成规则](#%E9%89%B4%E6%9D%83%E6%96%B9%E6%B3%95) |
| 401 | 签名参数解析失败 | {“message”:”HMAC signature cannot be verified”} | 检查签名的各个参数是否有缺失是否正确，特别确认下复制的**api\_key**是否正确 |
| 401 | 签名校验失败 | {“message”:”HMAC signature does not match”} | 签名验证失败，可能原因有很多。  
1\. 检查api\_key,api\_secret 是否正确。  
2.检查计算签名的参数host，date，request-line是否按照协议要求拼接。  
3\. 检查signature签名的base64长度是否正常(正常44个字节)。 |
| 403 | 时钟偏移校验失败 | {“message”:”HMAC signature cannot be verified, a valid date or x-date header is required for HMAC Authentication”} | 检查服务器时间是否标准，相差5分钟以上会报此错误 |

时钟偏移校验失败示例：

```json
HTTP/1.1 403 Forbidden
Date: Mon, 30 Nov 2020 02:34:33 GMT
Content-Length: 116
Content-Type: text/plain; charset=utf-8
{
    "message": "HMAC signature does not match, a valid date or x-date header is required for HMAC Authentication"
}
```

### [#](#请求参数-创建声纹特征库) 请求参数（创建声纹特征库）

在调用业务接口时，都需要在 Http Request Body 中配置以下参数，请求数据均为json字符串。 请求参数示例：

```json
{
  "header": {
    "app_id": "your_app_id",
    "status": 3
  },
  "parameter": {
    "s782b4996": {
      "func": "createGroup",
      "groupId": "iFLYTEK_examples_groupId",
      "groupName": "iFLYTEK_examples_groupName",
      "groupInfo": "iFLYTEK_examples_groupInfo",
      "createGroupRes": {
        "encoding": "utf8",
        "compress": "raw",
        "format": "json"
      }
    }
  }
}
```

| 参数名 | 类型 | 必传 | 描述 |
| --- | --- | --- | --- |
| header | object | 是 | 用于上传平台参数 |
| header.app\_id | string | 是 | 在平台申请的appid信息 |
| header.status | int | 是 | 请求状态，取值为：3（一次传完） |
| parameter | object | 是 | 用于上传服务特性参数 |
| parameter.s782b4996 | object | 是 | 用于上传功能参数 |
| parameter.s782b4996.func | string | 是 | 用于指定声纹的具体能力（创建声纹特征库值为createGroup） |
| parameter.s782b4996.groupId | string | 是 | 创建分组的标识，支持字母数字下划线，长度最大为32 |
| parameter.s782b4996.groupName | string | 否 | 创建分组的名称，长度最小为0，最大为256 |
| parameter.s782b4996.groupInfo | string | 否 | 创建分组的描述信息，长度最小为0，最大为256 |
| parameter.s782b4996.createGroupRes | object | 是 | 期望返回结果的格式 |
| parameter.s782b4996.createGroupRes.encoding | string | 是 | 编码格式（固定utf-8） |
| parameter.s782b4996.createGroupRes.compress | string | 是 | 压缩格式（固定raw） |
| parameter.s782b4996.createGroupRes.format | string | 是 | 文本格式（固定json） |

### [#](#返回参数-创建声纹特征库) 返回参数（创建声纹特征库）

返回参数示例：

```json
{
  "header": {
    "code": 0,
    "message": "success",
    "sid": "ase000e55f5@hu178fca72b160210882"
  },
  "payload": {
    "createGroupRes": {
      "text": "eyJncm91cEl..."
    }
  }
}
```

text字段Base64解码后示例：

```json
{
  "groupName": "iFLYTEK_examples_groupName",
  "groupId": "iFLYTEK_examples_groupId",
  "groupInfo": "iFLYTEK_examples_groupInfo"
}
```

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| header | object | 用于传递平台参数 |
| header.sid | string | 本次会话唯一标识id |
| header.code | int | 0表示会话调用成功（并不一定表示服务调用成功，服务是否调用成功以text字段为准）  
其它表示会话调用异常，详情请参考[错误码](#%E9%94%99%E8%AF%AF%E7%A0%81)。 |
| header.message | string | 描述信息 |
| payload | object | 数据段，用于携带响应的数据 |
| payload.createGroupRes | object | 响应数据块 |
| payload.createGroupRes.text | string | 响应数据base64编码 |

**payload.createGroupRes.text字段base64解码后信息如下，请重点关注：**  

| 字段 | 类型 | 描述 | 备注 |
| --- | --- | --- | --- |
| groupId | string | 创建分组的唯一标识 |  |
| groupName | string | 创建分组的名称 |  |
| groupInfo | string | 创建分组的描述信息 |  |

### [#](#请求参数-添加音频特征) 请求参数（添加音频特征）

在调用业务接口时，都需要在 Http Request Body 中配置以下参数，请求数据均为json字符串。 请求参数示例：

```json
{
  "header": {
    "app_id": "your_app_id",
    "status": 3
  },
  "parameter": {
    "s782b4996": {
      "func": "createFeature",
      "groupId": "iFLYTEK_examples_groupId",
      "featureId": "iFLYTEK_examples_featureId",
      "featureInfo": "iFLYTEK_examples_featureInfo",
      "createFeatureRes": {
        "encoding": "utf8",
        "compress": "raw",
        "format": "json"
      }
    }
  },
  "payload": {
    "resource": {
      "encoding": "lame",
      "sample_rate": 16000,
      "channels": 1,
      "bit_depth": 16,
      "status": 3,
      "audio": "SUQzBAAAAAAAI1..."
    }
  }
}
```

| 参数名 | 类型 | 必传 | 描述 |
| --- | --- | --- | --- |
| header | object | 是 | 用于上传平台参数 |
| header.app\_id | string | 是 | 在平台申请的appid信息 |
| header.status | int | 是 | 请求状态，取值为：3（一次传完） |
| parameter | object | 是 | 用于上传服务特性参数 |
| parameter.s782b4996 | object | 是 | 用于上传功能参数 |
| parameter.s782b4996.func | string | 是 | 用于指定声纹的具体能力（添加音频特征值为createFeature） |
| parameter.s782b4996.groupId | string | 是 | 分组的标识，支持字母数字下划线，长度最大为32 |
| parameter.s782b4996.featureId | string | 是 | 特征的标识，长度最小为0，最大为32 |
| parameter.s782b4996.featureInfo | string | 否 | 特征描述信息，长度最小为0，最大为256（建议在特征信息里加入时间戳） |
| parameter.s782b4996.createFeatureRes | object | 是 | 期望返回结果的格式 |
| parameter.s782b4996.createFeatureRes.encoding | string | 是 | 编码格式（固定utf-8） |
| parameter.s782b4996.createFeatureRes.compress | string | 是 | 压缩格式（固定raw） |
| parameter.s782b4996.createFeatureRes.format | string | 是 | 文本格式（固定json） |
| payload | object | 是 | 用于上传请求数据 |
| payload.resource | object | 是 | 用于相关音频相关参数 |
| payload.resource.encoding | string | 是 | 音频编码（固定lame） |
| payload.resource.sample\_rate | int | 是 | 音频采样率（16000） |
| payload.resource.channels | int | 否 | 音频声道数（1单声道） |
| payload.resource.bit\_depth | int | 否 | 音频位深（16） |
| payload.resource.status | int | 是 | 音频数据状态（3一次性传完） |
| payload.resource.audio | string | 是 | 音频数据base64编码（编码后最小长度:1B 最大长度:4M） |

### [#](#返回参数-添加音频特征) 返回参数（添加音频特征）

返回参数示例：

```json
{
  "header": {
    "code": 0,
    "message": "success",
    "sid": "ase000ec93e@hu178fd5902750212882"
  },
  "payload": {
    "createFeatureRes": {
      "text": "eyJmZWF0dXJl..."
    }
  }
}
```

text字段Base64解码后示例：

```json
{
  "featureId": "iFLYTEK_examples_featureId"
}
```

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| header | object | 用于传递平台参数 |
| header.sid | string | 本次会话唯一标识id |
| header.code | int | 0表示会话调用成功（并不一定表示服务调用成功，服务是否调用成功以text字段为准）  
其它表示会话调用异常，详情请参考[错误码](#%E9%94%99%E8%AF%AF%E7%A0%81)。 |
| header.message | string | 描述信息 |
| payload | object | 数据段，用于携带响应的数据 |
| payload.createFeatureRes | object | 响应数据块 |
| payload.createFeatureRes.text | string | 响应数据base64编码 |

**payload.createFeatureRes.text字段base64解码后信息如下，请重点关注：**  

| 字段 | 类型 | 描述 | 备注 |
| --- | --- | --- | --- |
| featureId | string | 特征的唯一标识 |  |

### [#](#请求参数-更新音频特征) 请求参数（更新音频特征）

在调用业务接口时，都需要在 Http Request Body 中配置以下参数，请求数据均为json字符串。 请求参数示例：

```json
{
  "header": {
    "app_id": "your_app_id",
    "status": 3
  },
  "parameter": {
    "s782b4996": {
      "func": "updateFeature",
      "groupId": "iFLYTEK_examples_groupId",
      "featureId": "iFLYTEK_examples_featureId",
      "featureInfo": "iFLYTEK_examples_featureInfo_update",
      "updateFeatureRes": {
        "encoding": "utf8",
        "compress": "raw",
        "format": "json"
      }
    }
  },
  "payload": {
    "resource": {
      "encoding": "lame",
      "sample_rate": 16000,
      "channels": 1,
      "bit_depth": 16,
      "status": 3,
      "audio": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI3Lj..."
    }
  }
}
```

| 参数名 | 类型 | 必传 | 描述 |
| --- | --- | --- | --- |
| header | object | 是 | 用于上传平台参数 |
| header.app\_id | string | 是 | 在平台申请的appid信息 |
| header.status | int | 是 | 请求状态，取值为：3（一次传完） |
| parameter | object | 是 | 用于上传服务特性参数 |
| parameter.s782b4996 | object | 是 | 用于上传功能参数 |
| parameter.s782b4996.func | string | 是 | 用于指定声纹的具体能力（更新音频特征值为updateFeature） |
| parameter.s782b4996.groupId | string | 是 | 此次音频特征所存放的分组标识，支持字母数字下划线，长度最大为32 |
| parameter.s782b4996.featureId | string | 否 | 特征的标识，长度最小为0，最大为32 |
| parameter.s782b4996.featureInfo | string | 否 | 特征描述信息，长度最小为0，最大为256（建议在特征信息里加入时间戳） |
| parameter.s782b4996.cover | boolean | 否 | 更新方式，为true时表示覆盖原有的特征，为false时表示与原有的特征进行合并更新。默认为true |
| parameter.s782b4996.updateFeatureRes | object | 是 | 期望返回结果的格式 |
| parameter.s782b4996.updateFeatureRes.encoding | string | 是 | 编码格式（固定utf-8） |
| parameter.s782b4996.updateFeatureRes.compress | string | 是 | 压缩格式（固定raw） |
| parameter.s782b4996.updateFeatureRes.format | string | 是 | 文本格式（固定json） |
| payload | object | 是 | 用于上传请求数据 |
| payload.resource | object | 是 | 用于相关音频相关参数 |
| payload.resource.encoding | string | 是 | 音频编码（固定lame） |
| payload.resource.sample\_rate | int | 是 | 音频采样率（16000） |
| payload.resource.channels | int | 否 | 音频声道数（1单声道） |
| payload.resource.bit\_depth | int | 否 | 音频位深（16） |
| payload.resource.status | int | 是 | 音频数据状态（3一次性传完） |
| payload.resource.audio | string | 是 | 音频数据base64编码（编码后最小长度:1B 最大长度:4M） |

### [#](#返回参数-更新音频特征) 返回参数（更新音频特征）

返回参数示例：

```json
{
  "header": {
    "code": 0,
    "message": "success",
    "sid": "ase000d96a6@hu17a5ad256e70212882"
  },
  "payload": {
    "updateFeatureRes": {
      "status": "3",
      "text": "eyJtc2ciOiJzdWNjZXNzIn0="
    }
  }
}
```

text字段Base64解码后示例：

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| header | object | 用于传递平台参数 |
| header.sid | string | 本次会话唯一标识id |
| header.code | int | 0表示会话调用成功（并不一定表示服务调用成功，服务是否调用成功以text字段为准）  
其它表示会话调用异常，详情请参考[错误码](#%E9%94%99%E8%AF%AF%E7%A0%81)。 |
| header.message | string | 描述信息 |
| payload | object | 数据段，用于携带响应的数据 |
| payload.updateFeatureRes | object | 响应数据块 |
| payload.updateFeatureRes.text | string | 响应数据base64编码 |

**payload.updateFeatureRes.text字段base64解码后信息如下，请重点关注：**  

| 字段 | 类型 | 描述 | 备注 |
| --- | --- | --- | --- |
| msg | string | 更新信息 | success代表更新成功 |

### [#](#请求参数-查询特征列表) 请求参数（查询特征列表）

**注：查询结果可能受限制无法展示全部特征。**  
在调用业务接口时，都需要在 Http Request Body 中配置以下参数，请求数据均为json字符串。  
请求参数示例：

```json
{
  "header": {
    "app_id": "your_app_id",
    "status": 3
  },
  "parameter": {
    "s782b4996": {
      "func": "queryFeatureList",
      "groupId": "iFLYTEK_examples_groupId",
      "queryFeatureListRes": {
        "encoding": "utf8",
        "compress": "raw",
        "format": "json"
      }
    }
  }
}
```

| 参数名 | 类型 | 必传 | 描述 |
| --- | --- | --- | --- |
| header | object | 是 | 用于上传平台参数 |
| header.app\_id | string | 是 | 在平台申请的appid信息 |
| header.status | int | 是 | 请求状态，取值为：3（一次传完） |
| parameter | object | 是 | 用于上传服务特性参数 |
| parameter.s782b4996 | object | 是 | 用于上传功能参数 |
| parameter.s782b4996.func | string | 是 | 用于指定声纹的具体能力（查询特征列表值为queryFeatureList） |
| parameter.s782b4996.groupId | string | 是 | 查询特征所在的分组标识，支持字母数字下划线，长度最大为32 |
| parameter.s782b4996.queryFeatureListRes | object | 是 | 期望返回结果的格式 |
| parameter.s782b4996.queryFeatureListRes.encoding | string | 是 | 编码格式（固定utf-8） |
| parameter.s782b4996.queryFeatureListRes.compress | string | 是 | 压缩格式（固定raw） |
| parameter.s782b4996.queryFeatureListRes.format | string | 是 | 文本格式（固定json） |

### [#](#返回参数-查询特征列表) 返回参数（查询特征列表）

返回参数示例：

```json
{
  "header": {
    "code": 0,
    "message": "success",
    "sid": "ase000eebfc@hu178fd7c11f20212882"
  },
  "payload": {
    "queryFeatureListRes": {
      "text": "W3siZmVhdHVy..."
    }
  }
}
```

text字段Base64解码后示例：

```json
[
  {
    "featureInfo": "iFLYTEK_examples_featureInfo",
    "featureId": "iFLYTEK_examples_featureId"
  }
]
```

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| header | object | 用于传递平台参数 |
| header.code | int | 0表示会话调用成功（并不一定表示服务调用成功，服务是否调用成功以text字段为准）  
其它表示会话调用异常，详情请参考[错误码](#%E9%94%99%E8%AF%AF%E7%A0%81)。 |
| header.message | string | 描述信息 |
| header.sid | string | 本次会话唯一标识id |
| payload | object | 数据段，用于携带响应的数据 |
| payload.queryFeatureListRes | object | 响应数据块 |
| payload.queryFeatureListRes.text | string | 响应数据base64编码 |

**payload.queryFeatureListRes.text字段base64解码后信息如下，请重点关注：**  

| 字段 | 类型 | 描述 | 备注 |
| --- | --- | --- | --- |
| featureInfo | string | 特征描述（建议创建时加时间戳，方便查找对应音频信息） |  |
| featureId | string | 特征标识 |  |

### [#](#请求参数-特征比对1-1) 请求参数（特征比对1:1）

在调用业务接口时，都需要在 Http Request Body 中配置以下参数，请求数据均为json字符串。 请求参数示例：

```json
{
  "header": {
    "app_id": "your_app_id",
    "status": 3
  },
  "parameter": {
    "s782b4996": {
      "func": "searchScoreFea",
      "groupId": "iFLYTEK_examples_groupId",
      "dstFeatureId": "iFLYTEK_examples_featureId",
      "searchScoreFeaRes": {
        "encoding": "utf8",
        "compress": "raw",
        "format": "json"
      }
    }
  },
  "payload": {
    "resource": {
      "encoding": "lame",
      "sample_rate": 16000,
      "channels": 1,
      "bit_depth": 16,
      "status": 3,
      "audio": "SUQzBAAAAAAAI1RTU0UAA..."
    }
  }
}
```

| 参数名 | 类型 | 必传 | 描述 |
| --- | --- | --- | --- |
| header | object | 是 | 用于上传平台参数 |
| header.app\_id | string | 是 | 在平台申请的appid信息 |
| header.status | int | 是 | 请求状态，取值为：3（一次传完） |
| parameter | object | 是 | 用于上传服务特性参数 |
| parameter.s782b4996 | object | 是 | 用于上传功能参数 |
| parameter.s782b4996.func | string | 是 | 用于指定声纹的具体能力（特征比对1:1值为searchScoreFea） |
| parameter.s782b4996.groupId | string | 是 | 需要比对特征所存放的分组标识，支持字母数字下划线，长度最大为32 |
| parameter.s782b4996.dstFeatureId | string | 是 | 需要比对的特征的标识，长度最小为0，最大为32 |
| parameter.s782b4996.searchScoreFeaRes | object | 是 | 期望返回结果的格式 |
| parameter.s782b4996.searchScoreFeaRes.encoding | string | 是 | 编码格式（固定utf-8） |
| parameter.s782b4996.searchScoreFeaRes.compress | string | 是 | 压缩格式（固定raw） |
| parameter.s782b4996.searchScoreFeaRes.format | string | 是 | 文本格式（固定json） |
| payload | object | 是 | 用于上传请求数据 |
| payload.resource | object | 是 | 用于相关音频相关参数 |
| payload.resource.encoding | string | 是 | 音频编码（固定lame） |
| payload.resource.sample\_rate | int | 是 | 音频采样率（16000） |
| payload.resource.channels | int | 否 | 音频声道数（1单声道） |
| payload.resource.bit\_depth | int | 否 | 音频位深（16） |
| payload.resource.status | int | 是 | 音频数据状态（3一次性传完） |
| payload.resource.audio | string | 是 | 音频数据base64编码（编码后最小长度:1B 最大长度:4M） |

### [#](#返回参数-特征比对1-1) 返回参数（特征比对1:1）

返回参数示例：

```json
{
  "header": {
    "code": 0,
    "message": "success",
    "sid": "ase000e1142@hu178fd98935d0212882"
  },
  "payload": {
    "searchScoreFeaRes": {
      "text": "eyJhZ2UiOiJja..."
    }
  }
}
```

text字段Base64解码后示例：

```json
{
  "score": 1,
  "featureInfo": "iFLYTEK_examples_featureInfo",
  "featureId": "iFLYTEK_examples_featureId"
}
```

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| header | object | 用于传递平台参数 |
| header.sid | string | 本次会话唯一标识id |
| header.code | int | 0表示会话调用成功（并不一定表示服务调用成功，服务是否调用成功以text字段为准）  
其它表示会话调用异常，详情请参考[错误码](#%E9%94%99%E8%AF%AF%E7%A0%81)。  
 |
| header.message | string | 描述信息 |
| payload | object | 数据段，用于携带响应的数据 |
| payload.searchScoreFeaRes | object | 响应数据块 |
| payload.searchScoreFeaRes.text | string | 响应数据base64编码 |

**payload.searchScoreFeaRes.text字段base64解码后信息如下，请重点关注：**  

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| score | float | 正常相似度得分0~1，精确到小数点后两位。（相似度范围-1到1） |
| featureInfo | string | 目标特征的描述信息 |
| featureId | string | 目标特征的唯一标识 |

### [#](#请求参数-特征比对1-n) 请求参数（特征比对1:N）

在调用业务接口时，都需要在 Http Request Body 中配置以下参数，请求数据均为json字符串。 请求参数示例：

```json
{
  "header": {
    "app_id": "your_app_id",
    "status": 3
  },
  "parameter": {
    "s782b4996": {
      "func": "searchFea",
      "groupId": "iFLYTEK_examples_groupId",
      "topK": 2,
      "searchFeaRes": {
        "encoding": "utf8",
        "compress": "raw",
        "format": "json"
      }
    }
  },
  "payload": {
    "resource": {
      "encoding": "lame",
      "sample_rate": 16000,
      "channels": 1,
      "bit_depth": 16,
      "status": 3,
      "audio": "SUQzBAAAAAAAI1RTU0UAAAAPAAA..."
    }
  }
}
```

| 参数名 | 类型 | 必传 | 描述 |
| --- | --- | --- | --- |
| header | object | 是 | 用于上传平台参数 |
| header.app\_id | string | 是 | 在平台申请的appid信息 |
| header.status | int | 是 | 请求状态，取值为：3（一次传完） |
| parameter | object | 是 | 用于上传服务特性参数 |
| parameter.s782b4996 | object | 是 | 用于上传功能参数 |
| parameter.s782b4996.func | string | 是 | 用于指定声纹的具体能力（特征比对1:N值为searchFea） |
| parameter.s782b4996.groupId | string | 是 | 指定分组进行比对，支持字母数字下划线，长度最大为32 |
| parameter.s782b4996.topK | int | 是 | 期望返回的特征数目,最大为10（要有足够的特征数量） |
| parameter.s782b4996.searchFeaRes | object | 是 | 期望返回结果的格式 |
| parameter.s782b4996.searchFeaRes.encoding | string | 是 | 编码格式（固定utf-8） |
| parameter.s782b4996.searchFeaRes.compress | string | 是 | 压缩格式（固定raw） |
| parameter.s782b4996.searchFeaRes.format | string | 是 | 文本格式（固定json） |
| payload | object | 是 | 用于上传请求数据 |
| payload.resource | object | 是 | 用于相关音频相关参数 |
| payload.resource.encoding | string | 是 | 音频编码（固定lame） |
| payload.resource.sample\_rate | int | 是 | 音频采样率（16000） |
| payload.resource.channels | int | 否 | 音频声道数（1单声道） |
| payload.resource.bit\_depth | int | 否 | 音频位深（16） |
| payload.resource.status | int | 是 | 音频数据状态（3一次性传完） |
| payload.resource.audio | string | 是 | 音频数据base64编码（编码后最小长度:1B 最大长度:4M） |

### [#](#返回参数-特征比对1-n) 返回参数（特征比对1:N）

返回参数示例：

```json
{
  "header": {
    "code": 0,
    "message": "success",
    "sid": "ase000e3672@hu178fdb6c69d0210882"
  },
  "payload": {
    "searchFeaRes": {
      "text": "eyJhZ2UiOiJ5b..."
    }
  }
}
```

text字段Base64解码后示例：

```json
{
  "scoreList": [
    {
      "score": 1,
      "featureInfo": "iFLYTEK_examples_featureInfo1",
      "featureId": "iFLYTEK_examples_featureId1"
    },
    {
      "score": 0.85,
      "featureInfo": "iFLYTEK_examples_featureInfo",
      "featureId": "iFLYTEK_examples_featureId"
    }
  ]
}
```

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| header | object | 用于传递平台参数 |
| header.sid | string | 本次会话唯一标识id |
| header.code | int | 0表示会话调用成功（并不一定表示服务调用成功，服务是否调用成功以text字段为准）  
其它表示会话调用异常，详情请参考[错误码](#%E9%94%99%E8%AF%AF%E7%A0%81)。 |
| header.message | string | 描述信息 |
| payload | object | 数据段，用于携带响应的数据 |
| payload.searchFeaRes | object | 响应数据块 |
| payload.searchFeaRes.text | string | 响应数据base64编码 |

**payload.searchFeaRes.text字段base64解码后信息如下，请重点关注：**  

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| scoreList | array | 特征比对结果 |
| scoreList\[n\].score | float | 正常相似度得分0~1，精确到小数点后两位。（相似度范围-1到1） |
| scoreList\[n\].featureInfo | string | 目标特征的描述信息 |
| scoreList\[n\].featureId | string | 目标特征的唯一标识 |

### [#](#请求参数-删除指定特征) 请求参数（删除指定特征）

在调用业务接口时，都需要在 Http Request Body 中配置以下参数，请求数据均为json字符串。 请求参数示例：

```json
{
  "header": {
    "app_id": "your_app_id",
    "status": 3
  },
  "parameter": {
    "s782b4996": {
      "func": "deleteFeature",
      "groupId": "iFLYTEK_examples_groupId",
      "featureId": "iFLYTEK_examples_featureId",
      "deleteFeatureRes": {
        "encoding": "utf8",
        "compress": "raw",
        "format": "json"
      }
    }
  }
}
```

| 参数名 | 类型 | 必传 | 描述 |
| --- | --- | --- | --- |
| header | object | 是 | 用于上传平台参数 |
| header.app\_id | string | 是 | 在平台申请的appid信息 |
| header.status | int | 是 | 请求状态，取值为：3（一次传完） |
| parameter | object | 是 | 用于上传服务特性参数 |
| parameter.s782b4996 | object | 是 | 用于上传功能参数 |
| parameter.s782b4996.func | string | 是 | 用于指定声纹的具体能力（删除指定特征值为deleteFeatureRes） |
| parameter.s782b4996.groupId | string | 是 | 删除特征所在的分组标识，支持字母数字下划线，长度最大为32 |
| parameter.s782b4996.featureId | string | 是 | 所需要删除的特征标识，长度最小为1，最大为32 |
| parameter.s782b4996.deleteFeatureRes | object | 是 | 期望返回结果的格式 |
| parameter.s782b4996.deleteFeatureRes.encoding | string | 是 | 编码格式（固定utf-8） |
| parameter.s782b4996.deleteFeatureRes.compress | string | 是 | 压缩格式（固定raw） |
| parameter.s782b4996.deleteFeatureRes.format | string | 是 | 文本格式（固定json） |

### [#](#返回参数-删除指定特征) 返回参数（删除指定特征）

返回参数示例：

```json
{
  "header": {
    "code": 0,
    "message": "success",
    "sid": "ase000e75d9@hu178fdf66e290210882"
  },
  "payload": {
    "deleteFeatureRes": {
      "text": "eyJtc2ciOi..."
    }
  }
}
```

text字段Base64解码后示例：

| header | object | 用于传递平台参数 |
| --- | --- | --- |
| header.code | int | 0表示会话调用成功（并不一定表示服务调用成功，服务是否调用成功以text字段为准）  
其它表示会话调用异常，详情请参考[错误码](#%E9%94%99%E8%AF%AF%E7%A0%81)。 |
| header.message | string | 描述信息 |
| header.sid | string | 本次会话唯一标识id |
| payload | object | 数据段，用于携带响应的数据 |
| payload.deleteFeatureRes | object | 响应数据块 |
| payload.deleteFeatureRes.text | string | 响应数据base64编码 |

**payload.deleteFeatureRes.text字段base64解码后信息如下，请重点关注：**  

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| msg | string | 删除结果（删除成功时返回success） |

### [#](#请求参数-删除声纹特征库) 请求参数（删除声纹特征库）

在调用业务接口时，都需要在 Http Request Body 中配置以下参数，请求数据均为json字符串。 请求参数示例：

```json
{
  "header": {
    "app_id": "your_app_id",
    "status": 3
  },
  "parameter": {
    "s782b4996": {
      "func": "deleteGroup",
      "groupId": "iFLYTEK_examples_groupId",
      "deleteGroupRes": {
        "encoding": "utf8",
        "compress": "raw",
        "format": "json"
      }
    }
  }
}
```

| 参数名 | 类型 | 必传 | 描述 |
| --- | --- | --- | --- |
| header | object | 是 | 用于上传平台参数 |
| header.app\_id | string | 是 | 在平台申请的appid信息 |
| header.status | int | 是 | 请求状态，取值为：3（一次传完） |
| parameter | object | 是 | 用于上传服务特性参数 |
| parameter.s782b4996 | object | 是 | 用于上传功能参数 |
| parameter.s782b4996.func | string | 是 | 用于指定声纹的具体能力（删除声纹特征库值为deleteGroup） |
| parameter.s782b4996.groupId | string | 是 | 删除分组的标识，支持字母数字下划线，长度最大为32 |
| parameter.s782b4996.deleteGroupRes | object | 是 | 期望返回结果的格式 |
| parameter.s782b4996.deleteGroupRes.encoding | string | 是 | 编码格式（固定utf-8） |
| parameter.s782b4996.deleteGroupRes.compress | string | 是 | 压缩格式（固定raw） |
| parameter.s782b4996.deleteGroupRes.format | string | 是 | 文本格式（固定json） |

### [#](#返回参数-删除声纹特征库) 返回参数（删除声纹特征库）

返回参数示例：

```json
{
  "header": {
    "code": 0,
    "message": "success",
    "sid": "ase000dcbc0@hu17a5ae64ab30212882"
  },
  "payload": {
    "deleteGroupRes": {
      "status": "3",
      "text": "eyJtc2ciOiJzdWNjZXNzIn0="
    }
  }
}
```

text字段Base64解码后示例：

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| header | object | 用于传递平台参数 |
| header.sid | string | 本次会话唯一标识id |
| header.code | int | 0表示会话调用成功（并不一定表示服务调用成功，服务是否调用成功以text字段为准）  
其它表示会话调用异常，详情请参考[错误码](#%E9%94%99%E8%AF%AF%E7%A0%81)。 |
| header.message | string | 描述信息 |
| payload | object | 数据段，用于携带响应的数据 |
| payload.deleteGroupRes | object | 响应数据块 |
| payload.deleteGroupRes.text | string | 响应数据base64编码 |

**payload.deleteGroupRes.text字段base64解码后信息如下，请重点关注：**  

| 字段 | 类型 | 描述 | 备注 |
| --- | --- | --- | --- |
| msg | string | 删除特征库是否成功 | success表示删除成功 |

## [#](#错误码) 错误码

备注：如出现下述列表中没有的错误码，可到 [这里 (opens new window)](https://www.xfyun.cn/document/error-code) 查询。

| 错误码 | 错误描述 | 说明 | 处理方法 |
| --- | --- | --- | --- |
| 10009 | input invalid data | 输入数据非法 | 检查输入的数据 |
| 10160 | parse request json error | 请求数据格式非法 | 检查请求数据是否是合法的json |
| 10161 | parse base64 string error | base64解码失败 | 检查发送的数据是否使用base64编码了 |
| 10313 | invalid appid | appid和apikey不匹配 | 检查appid是否合法 |
| 23005 | failed to create feature detail | 创建特征失败 | 检查是否创建声纹特征库 |
| 23006 | failed to delete feature detail | 删除特征失败 | 请查看删除的特征ID是否已经删除 |

## [#](#调用示例) 调用示例

[声纹识别demo java语言 (opens new window)](https://xfyun-doc.xfyun.cn/1626402142876728/voiceprint_recognition_java_demo.zip)

[声纹识别demo python语言 (opens new window)](https://xfyun-doc.xfyun.cn/1629079477078337/voiceprint_recognition_python_demo.zip)

*注：* 其他开发语言请参照 [接口调用流程](#%E6%8E%A5%E5%8F%A3%E8%B0%83%E7%94%A8%E6%B5%81%E7%A8%8B) 进行开发，也欢迎热心的开发者到 [讯飞开放平台社区 (opens new window)](http://bbs.xfyun.cn/portal.php) 分享你们的demo。

## [#](#常见问题) 常见问题

#### [#](#声纹识别1-1与1-n有什么区别) 声纹识别1:1与1:N有什么区别？

> 答：1:1模式主要做身份验证，主要证明你是你，主要应用场景为实名制场景（例如声纹解锁、声纹支付等）。而1:N模式则是验证你是谁，应用场景有办公考勤、会议签到等。

#### [#](#声纹的识别是否需要读固定的文本-文本有什么限制) 声纹的识别是否需要读固定的文本，文本有什么限制？

> 答：不需要读固定的文本，文本没有限制。

#### [#](#声纹识别得分在什么范围可以判定验证通过) 声纹识别得分在什么范围可以判定验证通过？

> 答：建议的参考得分范围为0.6-1可以判定验证通过，具体可以结合应用场景的安全性要求做进一步判断。

#### [#](#不同appid可以创建名称相同的声纹特征库吗) 不同appid可以创建名称相同的声纹特征库吗？

> 答：可以，每个appid的声纹特征库是相互独立的。