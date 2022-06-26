import {
  BackTop,
  Card,
  Divider,
  Input,
  List,
  Radio,
  Space,
  Tabs,
  Typography,
} from "antd";
import React, { useState } from "react";
import "./App.css";

const { TabPane } = Tabs;
const { Search } = Input;
const { Title, Paragraph, Text, Link } = Typography;

function MoreInfo(params) {
  console.log(params);
  const [count, setCount] = useState(params.count);
  if (params.item.length === 0) {
    return null;
  }
  function expend() {
    if (params.count >= params.item.length) {
      return null;
    } else if (count < params.item.length) {
      return (
        <Link
          onClick={() => {
            setCount(params.item.length);
          }}
        >
          展开
        </Link>
      );
    } else {
      return (
        <Link
          onClick={() => {
            setCount(params.count);
          }}
        >
          折叠
        </Link>
      );
    }
  }

  return (
    <Paragraph>
      <Text>{params.title}：</Text>
      <Space split={<Divider type="vertical" />} wrap>
        {params.item.slice(0, count).map((v, index) => (
          <Text key={index}>{v}</Text>
        ))}
        {expend()}
      </Space>
    </Paragraph>
  );
}

function App() {
  const [textListData, setTextListData] = useState([]);
  const [imgListData, setImgListData] = useState([]);
  const [checked, setChecked] = useState("tfidf");

  const onRadioChange = e => {
    console.log("radio checked", e.target.value);
    setChecked(e.target.value);
  };

  const onSearch = async value => {
    const response = await fetch(`api/search?q=${value}&f=${checked}`);
    let data = await response.text();
    try {
      data = JSON.parse(data);
    } catch (error) {
      console.log(error);
    }
    console.log(data);
    setTextListData(data);
  };

  const onSearchImg = async value => {
    const response = await fetch(`api/searchimg?q=${value}`);
    let data = await response.text();
    try {
      data = JSON.parse(data);
    } catch (error) {
      console.log(error);
    }
    console.log(data);
    setImgListData(data);
  };

  return (
    <div className="App">
      <BackTop />
      <Tabs defaultActiveKey="1">
        <TabPane tab="文字搜索" key="1">
          <Space direction="vertical" size="middle" style={{ display: "flex" }}>
            <Search
              placeholder="input search text"
              onSearch={onSearch}
              enterButton
            />
            <Radio.Group onChange={onRadioChange} value={checked}>
              <Radio value={"tfidf"}>tfidf</Radio>
              <Radio value={"bm25"}>bm25</Radio>
            </Radio.Group>
            <List
              header={<div>查询结果如下</div>}
              footer={<div>查询结束</div>}
              bordered
              itemLayout="horizontal"
              dataSource={textListData}
              renderItem={item => (
                <List.Item>
                  <Typography>
                    <Title level={5}>{item.title}</Title>
                    <Paragraph>
                      <Text>{item.time}</Text>
                      <Divider type="vertical" />
                      <Text>原文链接：</Text>
                      <Link href={item.url} target="_blank">
                        {item.url}
                      </Link>
                    </Paragraph>
                    <Paragraph
                      ellipsis={{
                        rows: 2,
                        expandable: true,
                      }}
                    >
                      <Text>相关内容</Text>： {item.relate}
                    </Paragraph>
                    <MoreInfo title="机构名称" item={item.org} count={5} />
                    <MoreInfo title="人名" item={item.name} count={5} />
                    <MoreInfo title="地址" item={item.address} count={5} />
                    <MoreInfo title="链接" item={item.urls} count={5} />
                  </Typography>
                </List.Item>
              )}
            />
          </Space>
        </TabPane>
        <TabPane tab="图片搜索" key="2">
          <Space direction="vertical" size="middle" style={{ display: "flex" }}>
            <Search
              placeholder="input search text"
              onSearch={onSearchImg}
              enterButton
            />
            <List
              header={<div>查询结果如下</div>}
              footer={<div>查询结束</div>}
              bordered
              grid={{
                xs: 1,
                sm: 2,
                md: 3,
                lg: 4,
                xl: 5,
                xxl: 6,
              }}
              dataSource={imgListData}
              renderItem={item => (
                <List.Item>
                  <Card cover={<img alt={item.des} src={item.img} />}>
                    <Card.Meta description={item.des} />
                    <Text>原文链接：</Text>
                    <Link href={item.href} target="_blank">
                      {item.href}
                    </Link>
                  </Card>
                </List.Item>
              )}
            />
          </Space>
        </TabPane>
      </Tabs>
    </div>
  );
}

export default App;
