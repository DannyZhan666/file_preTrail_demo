<template>
  <a-upload v-model:file-list="fileList" :customRequest="customUpload">
    <a-button>
      <upload-outlined></upload-outlined>
      Upload
    </a-button>
  </a-upload>
</template>
<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { UploadOutlined } from "@ant-design/icons-vue";
import axios from "axios";
import type { UploadProps, UploadFile } from "ant-design-vue";
import { filePage } from "@/api/client";

const fileList = ref<UploadProps["fileList"]>([]);

const fetchFiles = async () => {
  try {
    const response = await filePage();
    console.log("Response data:", response.data);

    if (response.data && Array.isArray(response.data.data)) {
      fileList.value = response.data.data.map((file) => ({
        uid: file.id.toString(),
        name: file.path.split("\\").pop(), // 获取文件名
        status: "done",
        response: "File uploaded successfully",
        url: file.path,
      }));
    } else {
      console.error(
        "Response data is not an array or undefined:",
        response.data
      );
      // 处理错误情况，例如显示错误消息或默认数据
    }
  } catch (error) {
    console.error("Error fetching files:", error);
  }
};

onMounted(() => {
  fetchFiles();
});
</script>

<style scoped></style>
