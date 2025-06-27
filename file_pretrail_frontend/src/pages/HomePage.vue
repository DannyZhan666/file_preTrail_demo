<template>
  <div id="homepage">
    <a-layout>
      <a-layout-header class="header">
        <GlobalHeader_user/>
      </a-layout-header>
      <a-layout-content class="content">
        <div class="block text-center">
          <el-carousel height="700px">
            <el-carousel-item v-for="(image, index) in images" :key="index">
              <img :src="image" alt="carousel image" class="carousel-image" />
            </el-carousel-item>
          </el-carousel>
        </div>
      </a-layout-content>
      <a-layout-footer class="footer">
        <a href="https://www.baidu.com" target="_blank">
          文件预审系统 by ckc
        </a>
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script setup lang="ts">
import GlobalHeader_user from "@/components/GlobalHeader_user.vue";
import {useLoginUserStore} from '@/store/useLoginUserStore'
import { ref, onMounted, onUnmounted } from 'vue';

const msg = "Welcome to Your Vue.js + TypeScript App";
const loginUserStore = useLoginUserStore();

const images = ref([
  new URL('@/assets/imgs/carousel_1.png', import.meta.url).href,
  new URL('@/assets/imgs/carousel_2.png', import.meta.url).href,
  new URL('@/assets/imgs/carousel_3.png', import.meta.url).href,
  new URL('@/assets/imgs/carousel_4.png', import.meta.url).href,
]);

onMounted(() => {
  loginUserStore.logout()
  console.log(loginUserStore.loginUser.userRole)
});

</script>

<style scoped>
#homepage .footer {
  background-color: #efefef;
  text-align: center;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
}

#homepage .content {
  padding: 20px;
  margin-bottom: 20px;
  background: linear-gradient(to right, #fefefe, #fff);
}

#homepage .header {
  background: white;
  margin-bottom: 16px;
  color: unset;
  padding-inline-start: 50px;
}

.demonstration {
  color: var(--el-text-color-secondary);
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 确保图片按比例缩放并居中 */
  display: block;
  margin: auto; /* 水平居中 */
}
.el-carousel__item {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
}

</style>
