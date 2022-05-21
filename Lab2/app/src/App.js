import { Input, Layout, List, Typography } from 'antd';
import { useState } from 'react';
import "./App.css";

const { Header, Footer, Content } = Layout;
const { Text } = Typography;
const { Search } = Input;

function App() {
  const [listData, setListData] = useState([])

  const onSearch = async (value) => {
    const response = await fetch(`api/search?q=${value}`);
    const data = await response.text();
    console.log(data);
    setListData([data]);
  }

  return (
    <div className="App">
      <Layout>
        <Header>Header</Header>
        <Content>
          <Search placeholder="input search text" onSearch={onSearch} enterButton />
          <List
            header={<div>标题</div>}
            footer={<div>尾注</div>}
            bordered
            dataSource={listData}
            renderItem={item => (
              <List.Item>
                <Text mark>[震惊！]</Text> {item}
              </List.Item>
            )}
          />
        </Content>
        <Footer>Footer</Footer>
      </Layout>
    </div>
  );
}

export default App;
