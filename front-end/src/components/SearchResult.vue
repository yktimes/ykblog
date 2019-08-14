<template>
  <div class="container">

    <!-- Modal: Edit Post -->
    <div data-backdrop="static" class="modal fade" id="editPostModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editPostModalTitle">Update Post</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">

            <form id="editPostForm" @submit.prevent="onSubmitUpdatePost" @reset.prevent="onResetUpdatePost">
              <div class="form-group" v-bind:class="{'u-has-error-v1': editPostForm.titleError}">
                <input type="text" v-model="editPostForm.title" class="form-control" id="editPostFormTitle" placeholder="标题">
                <small class="form-control-feedback" v-show="editPostForm.titleError">{{ editPostForm.titleError }}</small>
              </div>
              <div class="form-group">
                <input type="text" v-model="editPostForm.summary" class="form-control" id="editPostFormSummary" placeholder="摘要">
              </div>
              <div class="form-group">
                <textarea v-model="editPostForm.body" class="form-control" id="editPostFormBody" rows="5" placeholder=" 内容"></textarea>
                <small class="form-control-feedback" v-show="editPostForm.bodyError">{{ editPostForm.bodyError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Update</button>
            </form>

          </div>
        </div>
      </div>
    </div>

    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> 查询结果 <small v-if="datalist">(共 {{ count }} 篇, {{ page_total }} 页)</small>
        </h3>

        <div class="dropdown g-mb-10 g-mb-0--md">
          <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i class="icon-options-vertical g-pos-rel g-top-1"></i>
          </span>
          <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">

            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
              <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 5 篇
            </router-link>
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
              <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 10 篇
            </router-link>

            <div class="dropdown-divider"></div>

            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
              <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 20 篇
            </router-link>

          </div>
        </div>
      </div>
      <!-- End Panel Header -->

      <!-- Panel Body -->
      <div v-if="datalist" class="card-block g-pa-0" >

        <div class="media g-brd-around g-brd-gray-light-v4 g-brd-left-1 g-pa-20 g-mb-20"
          v-for="(post, index) in datalist" v-bind:key="index">


          <router-link v-bind:to="{ path: `/user/${post.object.author.id}` }" v-bind:title="post.object.author.name || post.object.author.username">

            <img  class="d-flex g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded-circle rounded mCS_img_loaded g-mt-3 g-mr-15" v-bind:src="post.object.author.avatar" v-bind:alt="post.object.author.name || post.object.author.username">
          </router-link>

          <div class="media-body">
            <div class="g-mb-15">
              <h5 class="h5 g-color-gray-dark-v1 mb-0"><router-link v-bind:to="{ path: `/user/${post.object.author.id}` }" class="g-text-underline--none--hover">{{ post.object.author.name || post.object.author.username }}</router-link> <span class="h6">发布了文章<router-link v-bind:to="{ name: 'PostDetail', params: { id: post.object.id }, query: { q: $route.query.q, page: $route.query.page, per_page: $route.query.per_page } }" class="g-text-underline--none--hover">《<span v-html="post.object.title"></span>》</router-link></span></h5>
              <span class="g-color-gray-dark-v4 g-font-size-12">{{ $moment(post.object.timestamp).format('YYYY年MM月DD日 HH:mm:ss') }}</span>
            </div>

            <!-- vue-markdown 开始解析markdown，它是子组件，通过 props 给它传值即可
            v-highlight 是自定义指令，用 highlight.js 语法高亮 -->
            <vue-markdown
              :source="post.object.summary"
              class="markdown-body g-mb-15"
              v-highlight>
            </vue-markdown>

            <div class="d-flex justify-content-start">
              <ul class="list-inline mb-0">
                <li class="list-inline-item g-mr-20">
                  <a class="g-color-gray-dark-v5 g-text-underline--none--hover" href="javascript:;">
                    <i class="icon-eye g-pos-rel g-top-1 g-mr-3"></i> {{ post.object.views }}
                  </a>
                </li>
                <li class="list-inline-item g-mr-20">
                  <router-link v-bind:to="{ path: `/post/${post.object.id}#like-post` }" class="g-color-gray-dark-v5 g-text-underline--none--hover">
                    <i class="icon-heart g-pos-rel g-top-1 g-mr-3"></i> {{ post.object.likers_count }}
                  </router-link>
                </li>
                <li class="list-inline-item g-mr-20">
                  <router-link v-bind:to="{ path: `/post/${post.object.id}#comment-list-wrap` }" class="g-color-gray-dark-v5 g-text-underline--none--hover">
                    <i class="icon-bubble g-pos-rel g-top-1 g-mr-3"></i> {{ post.object.comments_count }}
                  </router-link>
                </li>
              </ul>
              <ul class="list-inline mb-0 ml-auto">
                <li class="list-inline-item g-mr-5">
                  <router-link v-bind:to="{ name: 'PostDetail', params: { id: post.object.id }, query: { q: $route.query.q, page: $route.query.page, per_page: $route.query.per_page } }" class="btn btn-xs u-btn-outline-primary">阅读全文</router-link>
                </li>
                <li v-if="post.object.author.id == sharedState.user_id || sharedState.user_perms" class="list-inline-item g-mr-5">
                  <button v-on:click="onEditPost(post.object)" class="btn btn-xs u-btn-outline-purple" data-toggle="modal" data-target="#editPostModal">编辑</button>
                </li>
                <li v-if="post.object.author.id == sharedState.user_id || sharedState.user_perms" class="list-inline-item">
                  <button v-on:click="onDeletePost(post.object)" class="btn btn-xs u-btn-outline-red">删除</button>
                </li>
              </ul>
            </div>
          </div>
        </div>

      </div>
      <!-- End Panel Body -->
    </div>

    <!-- Pagination #04 -->
    <div v-if="datalist">
      <pagination
        v-bind:cur-page="page"
        v-bind:per-page="per_page"
        v-bind:total-pages="page_total">
      </pagination>
    </div>
    <!-- End Pagination #04 -->

  </div>
</template>

<script>
import store from '../store'
import Post from './Base/Post'
import Pagination from './Base/Pagination'
// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'
// bootstrap-markdown 编辑器依赖的 JS 文件，初始化编辑器在组件的 created() 方法中，同时它需要 JQuery 支持哦
import '../assets/bootstrap-markdown/js/bootstrap-markdown.js'
import '../assets/bootstrap-markdown/js/bootstrap-markdown.zh.js'
import '../assets/bootstrap-markdown/js/marked.js'


export default {
  name: 'SearchResult',  //this is the name of the component
  components: {
    Post,
    Pagination,
    VueMarkdown
  },
  data () {
    return {
      sharedState: store.state,
         page :1,
      per_page: 5,

      count:0,
      page_total:0,

      datalist:[],
      posts: '',
      postForm: {
        title: '',
        summary: '',
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null
      },
      editPostForm: {
        title: '',
        summary: '',
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null
      }
    }
  },
  methods: {
    getSearchResult () {
      let q = this.$route.query.q

      let path

       if (typeof this.$route.query.page != 'undefined') {
        this.page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        this.per_page = this.$route.query.per_page
      }

      if (typeof q != 'undefined') {
        path = `/api/search/?text=${q}&page=${this.page}&per_page=${this.per_page}`
      } else {
        path = `/api/search/?page=${this.page}&per_page=${this.per_page}`
      }

      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.posts = response.data.results
               this.datalist = response.data.results
          this.posts = response.data.data
          this.count=response.data.count
          this.page_total = Math.ceil(this.count/this.per_page)

          if (this.count > 0) {
            this.$toasted.success(response.data.message, { icon: 'fingerprint' })
          } else {
            this.$toasted.error('啊哦,没有搜索到啊.', { icon: 'fingerprint' })
          }
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.posts = ''
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },
    onEditPost (post) {
      // 不要使用对象引用赋值： this.editPostForm = post
      // 这样是同一个 post 对象，用户在 editPostForm 中的操作会双向绑定到该 post 上， 你会看到 modal 下面的博客也在变
      // 如果用户修改了一些数据，但是点了 cancel，你就必须在 onResetUpdatePost() 中重新加载一次博客列表，不然用户会看到修改后但未提交的不对称信息
      this.editPostForm = Object.assign({}, post)
    },
    onSubmitUpdatePost () {
      this.editPostForm.errors = 0  // 重置
      // 每次提交前先移除错误，不然错误就会累加
      $('#editPostForm .form-control-feedback').remove()
      $('#editPostForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')

      if (!this.editPostForm.title) {
        this.editPostForm.errors++
        this.editPostForm.titleError = 'Title is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        $('#editPostFormTitle').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editPostFormTitle').after('<small class="form-control-feedback">' + this.editPostForm.titleError + '</small>')
      } else {
        this.editPostForm.titleError = null
      }

      if (!this.editPostForm.body) {
        this.editPostForm.errors++
        this.editPostForm.bodyError = 'Body is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #postFormBody 上
        $('#editPostForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editPostForm .md-editor').after('<small class="form-control-feedback">' + this.editPostForm.bodyError + '</small>')
      } else {
        this.editPostForm.bodyError = null
      }

      if (this.editPostForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = `/api/posts/${this.editPostForm.id}/`
      const payload = {
        title: this.editPostForm.title,
        summary: this.editPostForm.summary,
        body: this.editPostForm.body
      }
      this.$axios.put(path, payload)
        .then((response) => {
          // 先隐藏 Modal
          $('#editPostModal').modal('hide')

          // handle success
          this.getSearchResult()
          this.$toasted.success('Successed update the post.', { icon: 'fingerprint' })
          this.editPostForm.title = '',
          this.editPostForm.summary = '',
          this.editPostForm.body = ''
        })
        .catch((error) => {
          // handle error
          for (var field in error.response.data.message) {
            if (field == 'title') {
              this.editPostForm.titleError = error.response.data.message[field]
              // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
              $('#editPostFormTitle').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
              $('#editPostFormTitle').after('<small class="form-control-feedback">' + this.editPostForm.titleError + '</small>')
            } else if (field == 'body') {
              this.editPostForm.bodyError = error.response.data.message[field]
              // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
              // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #postFormBody 上
              $('#editPostForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
              $('#editPostForm .md-editor').after('<small class="form-control-feedback">' + this.editPostForm.bodyError + '</small>')
            } else {
              this.$toasted.error(error.response.data.message[field], { icon: 'fingerprint' })
            }
          }
        })
    },
    onResetUpdatePost () {
      // 先移除错误
      $('#editPostForm .form-control-feedback').remove()
      $('#editPostForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
      // 再隐藏 Modal
      $('#editPostModal').modal('hide')
      // this.getSearchResult()
      this.$toasted.info('Cancelled, the post is not update.', { icon: 'fingerprint' })
    },
    onDeletePost (post) {
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
        if(result.value) {
          const path = `/api/posts/${post.id}`
          this.$axios.delete(path)
            .then((response) => {
              // handle success
              this.$swal('Deleted', 'You successfully deleted this post', 'success')
              // this.$toasted.success('Successed delete the post.', { icon: 'fingerprint' })
              this.getSearchResult()
            })
            .catch((error) => {
              // handle error
              console.log(error.response.data)
              this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
            })
        } else {
          this.$swal('Cancelled', 'The post is safe :)', 'error')
        }
      })
    }
  },
  created () {
    this.getSearchResult()
    // 初始化 bootstrap-markdown 插件
    $(document).ready(function() {
      $("#postFormBody, #editPostFormBody").markdown({
        autofocus:false,
        savable:false,
        iconlibrary: 'fa',  // 使用Font Awesome图标
        language: 'zh'
      })
    })
  },
  // 当查询参数 page 或 per_page 变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    // 注意：要先执行 next() 不然 this.$route.query 还是之前的
    next()
    this.getSearchResult()
  }
}
</script>
