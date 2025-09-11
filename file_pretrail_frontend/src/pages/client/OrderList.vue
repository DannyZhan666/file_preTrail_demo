<template>
  <div>
    <!-- 操作面板 -->
    <el-card class="job-title">
      <div class="title-container">
        <h2 class="my-title">订单管理</h2>
      </div>
    </el-card>

    <!-- 订单列表 -->
    <el-card class="narrow-card">
      <el-table :data="orderList" class="my-el-table">
        <el-table-column label="序号" type="index" width="150" align="center" />
        <el-table-column prop="id" label="订单id" align="center" />
        <el-table-column prop="order_name" label="订单名" align="center" />
        <el-table-column prop="lawyer_name" label="律师名" align="center" />
        <el-table-column prop="clientDueDate" label="我的预期时间" align="center" />
        <el-table-column prop="lawyerDueDate" label="律师预期时间" align="center" />
        <el-table-column prop="createTime" label="订单创建时间" align="center" />
        <el-table-column label="操作" align="center">
          <template #default="scope">
            <el-button link type="primary" size="large" @click="viewDetails(scope.row.id)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-buttons">
        <el-button @click="handlePreviousPage" :disabled="page === 1">上一页</el-button>
        <el-button @click="handleNextPage">下一页</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import dayjs from 'dayjs';
import router from "@/router";
import myAxios from "@/request"; // Import dayjs for time formatting

const searchKey = ref('');
const orderList = ref([]);
const dialogShow = ref(false);
const form = ref({
  orderName: '',
  customerName: '',
  createTime: '',
});
const page = ref(1); // 当前页码，初始为1
const pageSize = ref(10); // 每页条数，初始为10

const fetchOrders = async () => {
  try {
    const response = await myAxios.get(`/order/listForClient?page=${page.value}&pageSize=${pageSize.value}`);
    if (response.data && response.data.code === 200) {
      // Format the createTime field
      orderList.value = response.data.data.data.map(order => ({
        ...order,
        clientDueDate: dayjs(order.client_due_date).format('YYYY-MM-DD'), // 格式化时间
        lawyerDueDate: dayjs(order.lawyer_due_date).format('YYYY-MM-DD'), // 格式化时间
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

const handleNextPage = () => {
  page.value += 1; // 下一页
  fetchOrders();
};

const handlePreviousPage = () => {
  if (page.value > 1) {
    page.value -= 1; // 上一页
    fetchOrders();
  }
};

const createOrder = () => {
  dialogShow.value = true;
};

const viewDetails = (id) => {
  // 跳转到详情页面
  router.push({
    name: 'orderDetails_client',
    params: {id: id}
  });
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
.job-title {
  width: 66% !important;
  margin: 0 auto;
  background-color: #fff !important;
  border-radius: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  padding: 1px;
}

.title-container {
  display: flex;
  justify-content: center;
}

/* 标题样式调整 */
.my-title {
  text-align: center;
  color: #1890ff !important;
  font-weight: bold;
  margin: 0 auto; /* 水平居中 */
  margin-bottom: 0px !important;
  font-size: 24px;
}

.narrow-card {
  width: 85% !important; /* 与标题卡片宽度一致 */
  margin: 0 auto; /* 水平居中 */
  background-color: #fff !important; /* 移除黄色背景 */
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05); /* 添加阴影提升层次感 */
  padding: 20px;
  min-height: 600px; /* 保证与标题卡片高度一致 */
}

/* 增加卡片间垂直间距 */
.job-title + .narrow-card {
  margin-top: 30px !important;
}

.my-el-table {
  width: 100%;
  margin-top: 20px;
}

.pagination-buttons {
  display: flex;
  justify-content: center; /* 居中对齐 */
  margin-top: 20px; /* 往下移一点 */
  gap: 10px; /* 按钮之间的间距 */
}

</style>