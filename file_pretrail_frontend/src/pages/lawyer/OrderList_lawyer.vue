<template>
  <div>
    <!-- 操作面板 -->
    <el-card class="narrow-card">
      <div>
        <h2 class="my-title">订单管理</h2>
        <el-input
            v-model="searchKey"
            style="width: 240px"
            @keyup.enter.native="refresh(1)"
            placeholder="订单号 / 客户名"
        ></el-input>
        <el-button type="primary" icon="el-icon-search" @click="refresh(1)">搜索</el-button>
        <el-button type="primary" @click="createOrder()">创建订单</el-button>
      </div>
    </el-card>

    <!-- 订单列表 -->
    <el-card class="narrow-card">
      <el-table :data="orderList" class="my-el-table">
        <el-table-column label="序号" type="index" width="150" align="center" />
        <el-table-column prop="id" label="订单id" align="center" />
        <el-table-column prop="orderName" label="订单名" align="center" />
        <el-table-column prop="lawyerId" label="律师id" align="center" />
        <el-table-column prop="clientId" label="客户id" align="center" />
        <el-table-column prop="jid" label="工单id" align="center" />
        <el-table-column prop="createTime" label="创建时间" align="center" />
        <el-table-column label="操作" align="center">
          <template #default="scope">
            <el-popconfirm title="确定删除吗？" @confirm="deleteOrder(scope.row.id)">
              <el-button type="danger" slot="reference">删除</el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import dayjs from 'dayjs'; // Import dayjs for time formatting

const searchKey = ref('');
const orderList = ref([]);
const dialogShow = ref(false);
const form = ref({
  orderName: '',
  customerName: '',
  createTime: '',
});

const fetchOrders = async (page = 1, pageSize = 10) => {
  try {
    const response = await axios.get(`/order/list?page=${page}&pageSize=${pageSize}`);
    if (response.data && response.data.code === 200) {
      // Format the createTime field
      orderList.value = response.data.data.list.map(order => ({
        ...order,
        createTime: dayjs(order.createTime).format('YYYY-MM-DD HH:mm:ss'), // Format time
      }));
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error fetching orders:', error);
    ElMessage.error('获取订单列表失败');
  }
};

const createOrder = () => {
  dialogShow.value = true;
};

const submitOrder = async () => {
  try {
    const response = await axios.post(`/order/create`, form.value);
    if (response.data && response.data.code === 200) {
      dialogShow.value = false;
      form.value = { orderName: '', customerName: '', createTime: '' };
      fetchOrders();
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error submitting order:', error);
  }
};

const deleteOrder = async (id) => {
  try {
    const response = await axios.delete(`/order/delete/${id}`);
    if (response.data && response.data.code === 200) {
      fetchOrders();
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error deleting order:', error);
  }
};

const refresh = (page) => {
  fetchOrders(page);
};

onMounted(() => {
  fetchOrders();
});
</script>

<style scoped>
.narrow-card {
  width: 70%; /* 设置卡片宽度为页面宽度的80% */
  margin: 10px 300px; /* 居中显示 */
}

.my-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.buy {
  float: right;
  margin-right: 20px;
  margin-bottom: 10px;
}

.mid-input {
  width: 100%;
}

.create-dialog-btn {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.my-el-table {
  width: 100%;
  margin-top: 20px;
}
</style>