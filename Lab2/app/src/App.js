import { Space, Input, List, Typography, Divider } from "antd";
import { useState } from "react";
import "./App.css";

const { Search } = Input;
const { Title, Paragraph, Text, Link } = Typography;

function App() {
  const [listData, setListData] = useState([]);

  const onSearch = async value => {
    const response = await fetch(`api/search?q=${value}`);
    let data = await response.text();
    try {
      data = JSON.parse(data);
    } catch (error) {
      console.log(error);
    }
    console.log(data);
    setListData(data);
  };

  return (
    <div className="App">
      <Space direction="vertical" size="middle" style={{ display: "flex" }}>
        <Search
          placeholder="input search text"
          onSearch={onSearch}
          enterButton
        />
        <List
          header={<div>查询结果如下</div>}
          footer={<div>查询结束</div>}
          bordered
          itemLayout="horizontal"
          dataSource={listData}
          renderItem={item => (
            <List.Item>
              <Typography>
                <Title level={5}>{item.title}</Title>
                <Paragraph>
                  <Text>{item.time}</Text>
                  <Divider type="vertical"></Divider>
                  <Text>原文链接：</Text>
                  <Link href={item.url}>{item.url}</Link>
                </Paragraph>
                <Paragraph
                  ellipsis={{
                    rows: 2,
                    expandable: true,
                  }}
                >
                  {item.relate}
                </Paragraph>
              </Typography>
            </List.Item>
          )}
        />
      </Space>
    </div>
  );
}

export default App;
