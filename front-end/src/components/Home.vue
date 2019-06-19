<template>
  <div class="container">

    <!-- Modal: Edit Post -->
    <div class="modal fade" id="updatePostModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle"
         aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="updatePostModalTitle">Update Post</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">

            <form @submit.prevent="onSubmitUpdate" @reset.prevent="onResetUpdate">
              <div class="form-group" v-bind:class="{'u-has-error-v1': editForm.titleError}">
                <input type="text" v-model="editForm.title" class="form-control" id="editform_title" placeholder="标题">
                <small class="form-control-feedback" v-show="editForm.titleError">{{ editForm.titleError }}</small>
              </div>
              <div class="form-group">
                <input type="text" v-model="editForm.summary" class="form-control" id="editform_summary"
                       placeholder="摘要">
              </div>
              <div class="form-group">
                <textarea v-model="editForm.body" class="form-control" id="editform_body" rows="5"
                          placeholder=" 内容"></textarea>
                <small class="form-control-feedback" v-show="editForm.bodyError">{{ editForm.bodyError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Update</button>
            </form>

          </div>
        </div>
      </div>
    </div>

    <form v-if="sharedState.is_authenticated" @submit.prevent="onSubmitAdd" class="g-mb-40">
      <div class="form-group" v-bind:class="{'u-has-error-v1': postForm.titleError}">
        <input type="text" v-model="postForm.title" class="form-control" id="post_title" placeholder="标题">
        <small class="form-control-feedback" v-show="postForm.titleError">{{ postForm.titleError }}</small>
      </div>
      <div class="form-group">
        <input type="text" v-model="postForm.summary" class="form-control" id="post_summary" placeholder="摘要">
      </div>
      <div class="form-group">
        <textarea v-model="postForm.body" class="form-control" id="post_body" rows="5" placeholder=" 内容"></textarea>
        <small class="form-control-feedback" v-show="postForm.bodyError">{{ postForm.bodyError }}</small>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>


    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> All Posts
          <small v-if="count">(共 {{count}} 篇)</small>
        </h3>
        <div class="dropdown g-mb-10 g-mb-0--md">
          <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown"
                aria-haspopup="true" aria-expanded="false">
              <i class="icon-options-vertical g-pos-rel g-top-1"></i>
            </span>
          <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">
            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
              <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 5 篇
            </router-link>
            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
              <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 10 篇
            </router-link>
            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
              <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 20 篇
            </router-link>

            <div class="dropdown-divider"></div>

            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 1 }}" class="dropdown-item g-px-10">
              <i class="icon-plus g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 1 篇
            </router-link>

          </div>
        </div>
      </div>
      <!-- End Panel Header -->

      <!-- Panel Body -->
      <div v-if="datalist" class="card-block g-pa-0">
        <div v-for="(post, index) in datalist" v-bind:key="index"
             class="media g-brd-around g-brd-gray-light-v4 g-pa-20 g-mb-20">

          <!--<p>{{post}}</p>-->
          <router-link v-bind:to="{ name: 'Profile', params: { id: post.author.id }}"
                       v-bind:title="post.author.name || post.author.username">
            <img class="d-flex g-width-50 g-height-50 g-mt-3 g-mr-20" v-bind:src="post.author.avatar"
                 v-bind:alt="post.author.name || post.author.username">
          </router-link>

          <div class="media-body">
            <div class="d-sm-flex justify-content-sm-between align-items-sm-center g-mb-15 g-mb-10--sm">
              <h5 class="h4 g-font-weight-300 g-mr-10 g-mb-5 g-mb-0--sm">
                <router-link v-bind:to="{ name: 'Post', params: { id: post['id'] }}"
                             class="g-text-underline--none--hover">{{ post['title'] }}
                </router-link>
              </h5>
              <div class="text-nowrap g-font-size-12">
                <span>{{ $moment(post.timestamp).fromNow() }}</span> /
                <router-link v-bind:to="{ name: 'Profile', params: { id: post.author.id }}"><span
                  v-if="post.author.name">{{ post.author.name }}</span><span v-else>{{ post.author.username }}</span>
                </router-link>
              </div>
            </div>

            <!-- vue-markdown 开始解析markdown，它是子组件，通过 props 给它传值即可
            v-highlight 是自定义指令，用 highlight.js 语法高亮 -->
            <vue-markdown
              :source="post.summary"
              class="markdown-body g-mb-15"
              v-highlight>
            </vue-markdown>

            <div class="d-flex justify-content-start">
              <ul class="list-inline mb-0">
                <li class="list-inline-item g-mr-20">
                  <a class="g-color-gray-dark-v5 g-text-underline--none--hover" href="page-profile-comments-1.html#">
                    <i class="icon-eye g-pos-rel g-top-1 g-mr-3"></i> {{ post.views }}
                  </a>
                </li>
              </ul>
              <ul class="list-inline mb-0 ml-auto">
                <li class="list-inline-item g-mr-5">
                  <p>{{post['id']}}</p>
                  <router-link v-bind:to="{ name: 'Post', params: { id: post['id'] }}"
                               class="btn btn-xs u-btn-outline-primary">阅读全文
                  </router-link>
                </li>
                <li v-if="post.author.id == sharedState.user_id" class="list-inline-item g-mr-5">
                  <button v-on:click="onEditPost(post)" class="btn btn-xs u-btn-outline-purple" data-toggle="modal"
                          data-target="#updatePostModal">编辑
                  </button>
                </li>
                <li v-if="post.author.id == sharedState.user_id" class="list-inline-item">
                  <button v-on:click="onDeletePost(post)" class="btn btn-xs u-btn-outline-red">删除</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <!-- End Panel Body -->
    </div>


    <!-- Pagination #04 -->

    <nav aria-label="Page navigation example">
      <ul class="pagination justify-content-center">
        <li class="page-item">
          <a class="page-link" v-show="previous" @click="on_page(previous)">上一页</a>

        </li>


        <span v-for="num in page_nums">

      <li @click="on_page(num)" :class="num==page?'page-item active':'page-item'">
      <a class="page-link">{{num}}</a>
      </li>

     </span>


        <li class="page-item">
          <a class="page-link" v-show="next" @click="on_page(next)">下一页</a>

        </li>

      </ul>
    </nav>


  </div>
</template>

<script>
  import store from '../store'
  // 导入 vue-markdown 组件解析 markdown 原文为　HTML
  import VueMarkdown from 'vue-markdown'
  // bootstrap-markdown 编辑器依赖的 JS 文件，初始化编辑器在组件的 created() 方法中，同时它需要 JQuery 支持哦
  import '../assets/bootstrap-markdown/js/bootstrap-markdown.js'
  import '../assets/bootstrap-markdown/js/bootstrap-markdown.zh.js'
  import '../assets/bootstrap-markdown/js/marked.js'

  export default {
    name: 'Home',  //this is the name of the component
    components: {
      VueMarkdown
    },
    data() {
      return {

        page: 1, // 当前页数
        page_size: 5, // 每页数量
        sharedState: store.state,
        posts: '',
        datalist: [],
        count: 0,  // 总数量
        iter_pages: [],  // 分页导航栏
        postForm: {
          title: '',
          summary: '',
          body: '',
          errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
          titleError: null,
          bodyError: null
        },
        editForm: {
          title: '',
          summary: '',
          body: '',
          errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
          titleError: null,
          bodyError: null
        }
      }
    },

    computed: {
      total_page: function () {  // 总页数
        return Math.ceil(this.count / this.page_size);
      },
      next: function () {  // 下一页
        if (this.page >= this.total_page) {
          return 0;
        } else {
          return this.page + 1;
        }
      },
      previous: function () {  // 上一页
        if (this.page <= 0) {
          return 0;
        } else {
          return this.page - 1;
        }
      },
      page_nums: function () {  // 页码
        // 分页页数显示计算
        // 1.如果总页数<=5
        // 2.如果当前页是前3页
        // 3.如果当前页是后3页,
        // 4.既不是前3页，也不是后3页
        var nums = [];
        if (this.total_page <= 5) {
          for (var i = 1; i <= this.total_page; i++) {
            nums.push(i);
          }
        } else if (this.page <= 3) {
          nums = [1, 2, 3, 4, 5];
        } else if (this.total_page - this.page <= 2) {
          for (var i = this.total_page; i > this.total_page - 5; i--) {
            nums.push(i);
          }
        } else {
          for (var i = this.page - 2; i < this.page + 3; i++) {
            nums.push(i);
          }
        }
        return nums;
      }
    },
    methods: {
      getPosts() {



        this.$axios(`/api/posts/`,
          {
            params: {
              page: this.page,
              per_page: this.page_size,

            }
          }
          ,)
          .then((response) => {
            // handle success
            // TODO 我去，原来response.data还不行，我后端整体数据也叫data，得response.data.data
            // this.posts =response.data.data
            this.datalist = response.data.results
            this.count = response.data.count
            console.log(this.datalist)
            console.log(this.posts)
            console.log(this.count)


          })
          .catch((error) => {
            // handle error
            console.log(error)
          })
      },

      // 点击页数
      on_page: function (num) {
        if (num != this.page) {
          this.page = num;
          this.getPosts();
        }
      },
      onSubmitAdd(e) {
        this.postForm.errors = 0  // 重置
        if (!this.postForm.title) {
          this.postForm.errors++
          this.postForm.titleError = 'Title is required.'
          // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
          $('.md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        } else {
          this.postForm.titleError = null
        }


        if (!this.postForm.body) {
          this.postForm.errors++
          this.postForm.bodyError = 'Body is required.'
          // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
          $('.md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        } else {
          this.postForm.bodyError = null
        }
        if (this.postForm.errors > 0) {
          // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
          return false
        }
        const path = '/api/posts/'
        const payload = {
          title: this.postForm.title,
          summary: this.postForm.summary,
          body: this.postForm.body
        }
        this.$axios.post(path, payload)
          .then((response) => {
            // handle success
            this.getPosts()
            this.$toasted.success('Successed add a new post.', {icon: 'fingerprint'})
            this.postForm.title = '',
              this.postForm.summary = '',
              this.postForm.body = ''
          })
          .catch((error) => {
            // handle error
            console.log(error.response)
          })
      },
      onEditPost(post) {
        // 不要使用对象引用赋值： this.editForm = post
        // 这样是同一个 post 对象，用户在 editform 中的操作会双向绑定到该 post 上， 你会看到 modal 下面的博客也在变
        // 如果用户修改了一些数据，但是点了 cancel，你就必须在 onResetUpdate() 中重新加载一次博客列表，不然用户会看到修改后但未提交的不对称信息
        this.editForm = Object.assign({}, post)
      },
      onSubmitUpdate() {
        this.editForm.errors = 0  // 重置
        // 每次提交前先移除错误，不然错误就会累加
        $('.form-control-feedback').remove()
        $('.form-group.u-has-error-v1').removeClass('u-has-error-v1')
        if (!this.editForm.title) {
          this.editForm.errors++
          this.editForm.titleError = 'Title is required.'
          // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
          $('#editform_title').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
          $('#editform_title').after('<small class="form-control-feedback">' + this.editForm.titleError + '</small>')
        } else {
          this.editForm.titleError = null
        }
        if (!this.editForm.body) {
          this.editForm.errors++
          this.editForm.bodyError = 'Body is required.'
          // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
          // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
          $('.md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
          $('.md-editor').after('<small class="form-control-feedback">' + this.editForm.bodyError + '</small>')
        } else {
          this.editForm.bodyError = null
        }
        if (this.editForm.errors > 0) {
          // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
          return false
        }
        // 先隐藏 Modal
        $('#updatePostModal').modal('hide')
        const path = `/api/posts/${this.editForm.id}/`
        const payload = {
          title: this.editForm.title,
          summary: this.editForm.summary,
          body: this.editForm.body
        }
        this.$axios.put(path, payload)
          .then((response) => {
            // handle success
            this.getPosts()
            this.$toasted.success('Successed update the post.', {icon: 'fingerprint'})
            this.editForm.title = '',
              this.editForm.summary = '',
              this.editForm.body = ''
          })
          .catch((error) => {
            // handle error
            console.log(error.response)
          })
      },
      onResetUpdate() {
        // 先隐藏 Modal
        $('#updatePostModal').modal('hide')
        // this.getPosts()
        this.$toasted.info('Cancelled, the post is not update.', {icon: 'fingerprint'})
      },
      onDeletePost(post) {
        this.$swal({
          title: "Are you sure?",
          text: "该操作将彻底删除 [ " + post.title + " ], 请慎重",
          type: "warning",
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes, delete it!',
          cancelButtonText: 'No, cancel!'
        }).then((result) => {
          if (result.value) {
            const path = `/api/posts/${post.id}/`
            this.$axios.delete(path)
              .then((response) => {
                // handle success
                this.$swal('Deleted', 'You successfully deleted this post', 'success')
                // this.$toasted.success('Successed delete the post.', { icon: 'fingerprint' })
                this.getPosts()
              })
              .catch((error) => {
                // handle error
                console.log(error.response)
              })
          } else {
            this.$swal('Cancelled', 'The post is safe :)', 'error')
          }
        })
      }
    },
    mounted() {
      this.getPosts()
      // 初始化 bootstrap-markdown 插件
      $(document).ready(function () {
        $("#post_body, #editform_body").markdown({
          autofocus: false,
          savable: false,
          iconlibrary: 'fa',  // 使用Font Awesome图标
          language: 'zh'
        })
      })
    },
    // 当查询参数 page 或 per_page 变化后重新加载数据
    beforeRouteUpdate(to, from, next) {
      // 注意：要先执行 next() 不然 this.$route.query 还是之前的
      next()
      this.getPosts()
    }
  }
</script>
