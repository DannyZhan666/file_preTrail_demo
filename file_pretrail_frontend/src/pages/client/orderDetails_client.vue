<template>
  <div class="order-detail-content">
    <el-row :gutter="30">
      <!-- 左侧两栏 -->
      <el-col :span="12">
        <!-- 订单进度条部分 -->
        <el-card class="order-status-card">
          <div class="status-title">
            <h3>商家已发货，等待交易完成</h3>
            <div class="order-timeline">
              <el-timeline :reverse="true">
                <el-timeline-item timestamp="2019-12-13 15:00:50" :color="'#00B8B8'">
                  买家下单
                </el-timeline-item>
                <el-timeline-item timestamp="2019-12-13 15:05:00" :color="'#FF9B00'">
                  卖家发货
                </el-timeline-item>
                <el-timeline-item timestamp="2019-12-13 15:10:05" :color="'#B0B0B0'">
                  等待确认收货
                </el-timeline-item>
                <el-timeline-item timestamp="2019-12-13 15:15:00" :color="'#00B8B8'">
                  交易完成
                </el-timeline-item>
              </el-timeline>
            </div>
          </div>
        </el-card>

        <!-- 订单详情部分 -->
        <el-card class="order-info-card">
          <el-descriptions title="订单详情" :column="1" :size="size" border>
            <el-descriptions-item label="订单号">E2019121315000540270001</el-descriptions-item>
            <el-descriptions-item label="买家">张三</el-descriptions-item>
            <el-descriptions-item label="买家联系方式">13570440908</el-descriptions-item>
            <el-descriptions-item label="付款金额">￥0.01</el-descriptions-item>
            <el-descriptions-item label="支付方式">微信支付</el-descriptions-item>
            <el-descriptions-item label="支付时间">2019-12-13 15:10:05</el-descriptions-item>
            <el-descriptions-item label="卖家">李四</el-descriptions-item>
            <el-descriptions-item label="卖家联系方式">13570440909</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <!-- 右侧两栏 -->
      <el-col :span="12">
        <!-- 商品信息部分 -->
        <el-card class="product-info-card">
          <el-table :data="productData" style="width: 100%">
            <el-table-column label="商品名称" prop="name"></el-table-column>
            <el-table-column label="单价" prop="price"></el-table-column>
            <el-table-column label="数量" prop="quantity"></el-table-column>
            <el-table-column label="总价" prop="totalPrice"></el-table-column>
          </el-table>
        </el-card>

        <!-- 商家发货信息部分 -->
        <el-card class="seller-info-card">
          <el-descriptions title="商家信息" :column="1" :size="size" border>
            <el-descriptions-item label="商家名称">店铺名称</el-descriptions-item>
            <el-descriptions-item label="商家联系方式">13570440909</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>

    <!-- 返回列表按钮 -->
    <el-button class="back-button" type="primary" @click="goBack">返回列表</el-button>
  </div>
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue';
import {ElMessage} from 'element-plus';
import axios from "axios";
import {useRouter} from "vue-router";
import myAxios from "@/request";

const router = useRouter();

const productData = ref([
  {name: '测试样品', price: '￥0.01', quantity: 1, totalPrice: '￥0.01'}
]);

const size = ref('small');

const fetchJobDetails = async () => {
  try {
    const id = route.params.id;
    if (!id) throw new Error('无效的工单ID');

    const response = await myAxios.get(`/job/detailsForClient?id=${id}`);
    jobInfo.value = response.data.data;

    const blob = base64ToBlob(response.data.data.fileContent);
    pdfUrl.value = URL.createObjectURL(blob);

  } catch (err: any) {
    console.error('获取工单详情失败:', err);
    error.value = err.message || '获取工单信息失败';
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  // 跳转到订单列表页面
  router.push('/OrderList'); // 根据实际路由修改路径
};

onMounted(() => {
  fetchJobDetails();
});
</script>

<style scoped>
.order-detail-content {
  margin: 20px auto; /* 上下留 20px，左右居中 */
  max-width: 1200px; /* 设置页面最大宽度 */
  padding: 0 20px; /* 添加左右内边距，避免内容贴边 */
}

.order-status-card,
.order-info-card,
.product-info-card,
.seller-info-card {
  margin-bottom: 20px;
}

.status-title h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.order-timeline {
  margin-top: 10px;
}

.el-table th, .el-table td {
  text-align: center;
}

.el-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.back-button {
  position: fixed;
  bottom: 70px;
  right: 350px;
  z-index: 1000;
}
</style>