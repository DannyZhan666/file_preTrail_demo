<template>
  <div>
    <!-- 文件上传 -->
    <el-upload
      class="upload-demo"
      drag
      :on-success="handleSuccess"
      :before-upload="beforeUpload"
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">只能上传txt/pdf文件</div>
    </el-upload>

    <div class="uploaded-files">
      <h3>已上传的文件列表</h3>
      <el-table :data="fileList" style="width: 100%">
        <el-table-column prop="id" label="文件id" width="180">
        </el-table-column>
        <el-table-column prop="fileName" label="文件名" width="180">
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180">
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button @click="removeFile(scope.row.id)" type="text" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {ref, onMounted} from 'vue';

export default {
  setup() {
    const fileList = ref([]);

    const beforeUpload = (file) => {
      const isTxtOrPdf = file.type === 'application/pdf' || file.type === 'text/plain';
      const isLt2M = file.size / 1024 / 1024;

      if (!isTxtOrPdf) {
        this.$message.error('上传文件只能是 PDF/TXT 格式!');
      }
      if (!isLt2M) {
        this.$message.error('上传文件大小不能超过 1GB!');
      }

      // 创建 FormData 对象
      const formData = new FormData();
      formData.append('file', file);

      // 发送请求到后端
      axios.post(`/file/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          console.log(`上传进度：${progressEvent.loaded / progressEvent.total}`);
        }
      })
        .then(response => {
          // 假设后端返回的数据中包含文件信息
          fileList.value.push({
            id: response.data.id,
            name: file.name,
            url: response.data.url,
            createTime: response.data.createTime,
          });
          this.$message.success('上传成功');
          return true;
        })
        .catch(error => {
          console.error('Error uploading file:', error);
          this.$message.error('文件上传失败');
          return false;
        });

    };

    const handleSuccess = (response, file, fileList) => {
      // 假设后端返回的数据中包含文件信息
      fileList.value.push({
        id: response.data.id,
        name: file.name,
        url: response.data.url,
        createTime: response.data.createTime,
      });
    };

    const fetchFiles = async (page = 1, pageSize = 10) => {
      try {
        const response = await axios.get(`/file/pageByUser?page=${page}&pageSize=${pageSize}`);

        // 检查响应状态码和数据是否存在
        if (response.data && response.data.code === 200) {
          // console.log("----------------" + JSON.stringify(response.data.data));
          fileList.value = response.data.data.list.map((file) => ({
            id: file.id,
            path: file.path,
            fileName: file.fileName,
            createTime: file.createTime,
          }));
        } else {
          console.error('Invalid response data:', response.data);
          // 处理错误情况，例如显示错误消息或默认数据
        }
      } catch (error) {
        console.error('Error fetching files:', error);
      }
    };

    const removeFile = (id) => {
      fileList.value = fileList.value.filter(file => file.id !== id);
      // 也可以发送请求到后端删除文件
    };

    onMounted(() => {
      fetchFiles();
    });

    return {
      fileList,
      beforeUpload,
      handleSuccess,
      fetchFiles,
      removeFile,
    };
  },
};
</script>

<style scoped>
.upload-container {
  padding: 20px;
}

.file-table {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.file-table /deep/ .el-table__body {
  display: flex;
  flex-direction: column;
}

.file-table /deep/ .el-table__body-wrapper {
  overflow: hidden;
}

.file-table /deep/ .el-table__body tr {
  display: flex;
  flex-direction: row;
}

.file-table /deep/ .el-table__body td {
  flex: 1;
  padding: 10px;
  text-align: center;
  border-bottom: 1px solid #f0f0f0f0;
}

.file-table /deep/ .el-table__body tr:hover {
  background-color: #f5f7fa;
}
</style>

<!--<script>-->
<!--export default {-->
<!--  data() {-->
<!--    return {-->
<!--      types: [],-->
<!--      param: {-->
<!--        page: 1,-->
<!--        searchKey: '',-->
<!--        searchType: '',-->
<!--      },-->
<!--      addParam: {-->
<!--        fid: 1,-->
<!--        flower: '',-->
<!--        account: window.sessionStorage.getItem("token"),-->
<!--      },-->
<!--      list: [],-->
<!--      pagination: {-->
<!--        total: 1,-->
<!--        pageSize: 9,-->
<!--        currentPage: 1,-->
<!--      },-->
<!--    }-->
<!--  },-->
<!--  methods: {-->

<!--    pageChange(page) {-->
<!--      this.refresh(page);-->
<!--    },-->
<!--    addCart(flower) {-->
<!--      this.addParam.fid = flower.id;-->
<!--      this.addParam.flower = flower.name;-->
<!--      console.log(this.addParam)-->
<!--      this.$http.post("/cart/create", this.addParam).then(result => {-->
<!--        let R = result.data; // R-->
<!--        if (R.code === 2000) {-->
<!--          this.$message.success(R.msg);-->
<!--        } else {-->
<!--          this.$message.error(R.msg);-->
<!--        }-->
<!--      });-->
<!--    },-->
<!--    refresh(page) {-->
<!--      if (page === undefined) {-->
<!--        page = 1;-->
<!--      }-->
<!--      //window.sessionStorage.getItem('token')-->
<!--      this.$http.get("/flower/find?page=" + page + "&searchKey=" + this.param.searchKey-->
<!--        + "&searchType=" + this.param.searchType-->
<!--      ).then(result => {-->
<!--        let R = result.data;-->
<!--        this.list = R.data.items;-->
<!--        this.pagination.total = R.data.len;-->
<!--        this.pagination.currentPage = page;-->


<!--        console.log("total = " + this.pagination.total)-->
<!--        console.log("currentPage = " + this.pagination.currentPage)-->

<!--      })-->
<!--    },-->
<!--  },-->
<!--  created() {-->
<!--    this.refresh(1);-->
<!--  }-->
<!--}-->
<!--</script>-->

<!--<style scoped>-->
<!--.search-input {-->
<!--  width: 300px;-->
<!--}-->


<!--.updateForm {-->
<!--  width: 80%;-->
<!--}-->

<!--.btn-release {-->
<!--  float: right;-->
<!--  margin-top: 10px;-->
<!--  margin-right: 50px;-->
<!--}-->

<!--.form-releaseTask {-->
<!--  height: 300px;-->
<!--}-->

<!--.input-content-task {-->
<!--  width: 500px;-->
<!--}-->

<!--img {-->
<!--  margin-top: 10px;-->
<!--  width: 160px;-->
<!--  height: 160px;-->
<!--}-->

<!--.main-card {-->
<!--  background: #B3C0D1;-->
<!--}-->

<!--.button-add-cart {-->
<!--  float: right;-->
<!--  margin: 5px;-->
<!--}-->
<!--</style>-->
