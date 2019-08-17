<template>

  <div class="container " id="detail">

     <el-row  :gutter="30">
                <el-col :sm="30" :md="30" style="transition:all .5s ease-out;margin-bottom:30px;">

    <!-- Modal: Edit Post -->
    <div class="modal fade" id="updatePostModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
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
                <input type="text" v-model="editForm.summary" class="form-control" id="editform_summary" placeholder="摘要">
                                        <small class="form-control-feedback" v-show="editForm.summaryError">{{ editForm.summaryError }}</small>

              </div>

                       <div class="form-group">

<el-select v-model="editForm.category">

<el-option v-for="(item,index) in classListObj"
:label="item.name"
  :key="item.name"
:value="item.id"
  >
  </el-option>

  </el-select>

        <small class="form-control-feedback" v-show="editForm.categoryError">{{ editForm.categoryError }}</small>

              </div>


              <div class="form-group">

     <el-upload
  :action="imgUrl"

  ref='upload'
:on-success="imgSuccess"
  :limit="1"
  list-type="picture-card"

 >
  <i class="el-icon-plus"></i>
</el-upload>
<el-dialog :visible.sync="dialogVisible">
  <img width="100%" :src="dialogImageUrl" alt="">
</el-dialog>

</div>


              <div class="form-group">
                <textarea v-model="editForm.body" class="form-control" id="editPostFormBody" rows="5" placeholder=" 内容"></textarea>
                <small class="form-control-feedback" v-show="editForm.bodyError">{{ editForm.bodyError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Update</button>
            </form>

          </div>
        </div>
      </div>
    </div>
    <!-- End Modal: Edit Post -->


       <!-- Modal: Edit Comment -->
    <div class="modal fade" id="editCommentModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editCommentModalTitle">Update Comment</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">

            <form id="editCommentForm" @submit.prevent="onSubmitUpdateComment" @reset.prevent="onResetUpdateComment">
              <div class="form-group">
                <textarea v-model="editCommentForm.body" class="form-control" id="editCommentFormBody" rows="5" placeholder=" 评论内容"></textarea>
                <small class="form-control-feedback" v-show="editCommentForm.bodyError">{{ editCommentForm.bodyError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Update</button>
            </form>

          </div>
        </div>
      </div>
    </div>
    <!-- End Modal: Edit Comment -->



    <div class="row">
      <!-- Articles Content -->
      <div class="col-lg-9">

        <article class="g-mb-60 g-pt-15 g-pb-50">
          <header class="g-mb-30">
            <h1 class="g-color-primary g-mb-15 g-font-size-18">{{ post.title }}</h1>

            <ul class="list-inline d-sm-flex g-color-gray-dark-v4 mb-0">
              <li v-if="post.author && post.author.id == sharedState.user_id" class="list-inline-item">
                <button v-on:click="onEditPost(post)" class="btn btn-xs u-btn-outline-purple g-mr-5" data-toggle="modal" data-target="#updatePostModal">编辑</button>
              </li>
              <li v-if="post.author && post.author.id == sharedState.user_id" class="list-inline-item">
                <button v-on:click="onDeletePost(post)" class="btn btn-xs u-btn-outline-red g-mr-5">删除</button>
              </li>
              <li class="list-inline-item">
                <a href="#comment-list-wrap" class="btn btn-xs u-btn-outline-aqua g-mr-10">评论</a>
              </li>
              <li v-if="post.author" class="list-inline-item">
              <router-link v-bind:to="{ path: `/user/${post.author.id}/` }" class="u-link-v5 g-color-gray-dark-v4 g-color-primary--hover g-text-underline--none--hover"><span v-if="post.author.name">{{ post.author.name }}</span><span v-else>{{ post.author.username }}</span></router-link>
              </li>
              <li class="list-inline-item g-mx-10">/</li>
              <li class="list-inline-item">
                <i class="icon-clock"></i> {{ $moment(post.timestamp).format('YYYY年MM月DD日 HH:mm:ss') }}
              </li>
              <li class="list-inline-item g-mx-10">/</li>
              <li class="list-inline-item g-mr-10">
                <a class="u-link-v5 g-color-gray-dark-v4 g-color-primary--hover g-text-underline--none--hover" href="#comment-list-wrap">
                  <i class="icon-bubble"></i> {{comments.count}}
                </a>
              </li>
              <li class="list-inline-item ml-auto">
                <i class="icon-eye"></i> {{ post.views }} 次阅读
              </li>
            </ul>

            <hr class="g-brd-gray-light-v4 g-my-15">
          </header>


<!--<div class="el-image__placeholder">-->

<!--    <el-image :src="post.image"></el-image>-->
<!--  </div>-->

          <div id="postBody" class="g-font-size-16 g-line-height-1_8 g-mb-30">

            <!-- vue-markdown 开始解析markdown，它是子组件，通过 props 给它传值即可
            要指定TOC的级数哦，如果要修改TOC的样式，要在toc-rendered指定的函数中操作，因为要等它把TOC给创建出来
             -->
            <vue-markdown
              :source="post.body"
              :toc="showToc"
              :toc-first-level="1"
              :toc-last-level="3"
              v-on:toc-rendered="tocAllRight"
              toc-id="toc"
              class="markdown-body"
             >
            </vue-markdown>

          </div>


           <div id="like-post" class="row">
            <div class="col-lg-3">
              <button v-on:click="onLikeOrUnlikePost(post)" v-bind:class="btnOutlineColor" class="btn btn-block g-rounded-50 g-py-12 g-mb-10">
                <i class="icon-heart g-pos-rel g-top-1 g-mr-5"></i> 喜欢<span v-if="post.likers && post.likers.length > 0"> | {{ post.likers.length }}</span>
              </button>
            </div>
            <div class="col-lg-9">
              <ul v-if="post.likers" class="list-inline mb-0">
                <li class="list-inline-item"
                  v-for="(liker, index) in post.likers" v-bind:key="index">
                  <router-link
                    v-bind:to="{ path: `/user/${liker.id}` }"
                    v-bind:title="liker.name || liker.username">
                    <img class="g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded-circle rounded mCS_img_loaded g-mt-3" v-bind:src="liker.avatar" v-bind:alt="liker.name || liker.username">
                  </router-link>
                </li>
              </ul>
            </div>
          </div>

        </article>


        <!-- 博客文章的评论列表 -->
        <div id="comment-list-wrap" class="card border-0 g-mb-15">
          <!-- Panel Header -->
          <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
            <h3 class="h6 mb-0">
              <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> Comments
            </h3>
            <div class="dropdown g-mb-10 g-mb-0--md">
              <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="icon-options-vertical g-pos-rel g-top-1"></i>
              </span>
              <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">

                <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
                  <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 5 条顶层评论
                </router-link>
                <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
                  <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 10 条顶层评论
                </router-link>

                <div class="dropdown-divider"></div>

                <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
                  <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 20 条顶层评论
                </router-link>

              </div>
            </div>
          </div>
          <!-- End Panel Header -->

          <!-- Add Comment Form -->
          <form id="addCommentForm" v-if="sharedState.is_authenticated" @submit.prevent="onSubmitAddComment" @reset.prevent="onResetAddComment" class="g-mb-40">
            <div class="form-group">
              <textarea v-model="commentForm.body" class="form-control" id="commentFormBody" rows="5" placeholder=" 写下你的评论 ..."></textarea>
              <small class="form-control-feedback" v-show="commentForm.bodyError">{{ commentForm.bodyError }}</small>
            </div>
            <button type="reset" class="btn btn-secondary">Cancel</button>
            <button type="submit" class="btn btn-primary">Submit</button>
          </form>
          <!-- End Add Comment Form -->

          <div v-else class="btn-group g-mr-10 g-mb-50 g-px-10">
            <button type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              发表评论前，请先登录 ...
            </button>
            <div class="dropdown-menu" x-placement="bottom-start" style="position: absolute; transform: translate3d(0px, 35px, 0px); top: 0px; left: 0px; will-change: transform;">
              <router-link v-bind:to="{ path: '/login', query: { redirect: $route.fullPath } }" class="dropdown-item">站内账号</router-link>

            </div>
          </div>

          <!-- Panel Body -->
          <div v-if="comments" class="card-block g-pa-0" >

            <!-- 一级评论，按时间倒序排列 -->
            <div v-for="(comment, index) in comments.results" v-bind:key="index">

              <div v-bind:id="'c' + comment.id" class="comment-item media g-brd-around g-brd-gray-light-v4 g-pa-30 g-mb-20">
                <router-link v-bind:to="{ path: `/user/${comment.author.id}/` }">

                  <img class="d-flex g-width-50 g-height-50 rounded-circle g-brd-around g-brd-gray-light-v4 g-pa-2 g-mt-3 g-mr-15" v-bind:src="comment.author.avatar" v-bind:alt="comment.author.name || comment.author.username">

                </router-link>
                <div class="media-body">
                  <div class="g-mb-15">
                    <h5 v-if="comment.author.id == comment.post.author" class="h5 g-color-gray-dark-v1 mb-0"><router-link v-bind:to="{ path: `/user/${comment.author.id}/` }" class="comment-author g-text-underline--none--hover">{{ comment.author.name || comment.author.username }}</router-link> <button class="btn btn-xs u-btn-inset u-btn-outline-red g-mr-5">博文作者</button></h5>
                    <h5 v-else class="h5 g-color-gray-dark-v1 mb-0"><router-link v-bind:to="{ path: `/user/${comment.author.id}/` }" class="comment-author g-text-underline--none--hover">{{ comment.author.name || comment.author.username }}</router-link></h5>
                    <span class="g-color-gray-dark-v4 g-font-size-12">{{ $moment(comment.timestamp).format('YYYY年MM月DD日 HH:mm:ss') }}</span>
                  </div>

                  <div v-if="comment.disabled" class="g-color-red g-mb-15">此评论包含不良信息，已被禁止显示.</div>
                  <div v-else>
                    <!-- vue-markdown 开始解析markdown，它是子组件，通过 props 给它传值即可
                    v-highlight 是自定义指令，用 highlight.js 语法高亮 -->
                    <vue-markdown
                      :source="comment.body"
                      class="markdown-body g-mb-15"
                      v-highlight>
                    </vue-markdown>
                  </div>

                  <ul class="list-inline d-sm-flex my-0">
                    <li v-if="!comment.disabled" class="list-inline-item g-mr-20">
                      <a v-on:click="onLikeOrUnlike(comment)" class="u-link-v5 g-color-gray-dark-v4 g-color-primary--hover" href="javascript:;">
                        <i v-bind:class="{ 'g-color-red': comment.liked.indexOf(parseInt(sharedState.user_id)) != -1 }" class="icon-like g-pos-rel g-top-1 g-mr-3"></i>
                        <span v-if="comment.liked.length > 0"> {{ comment.liked.length }} 人赞</span>
                        <span v-else>赞</span>
                      </a>
                    </li>
                    <li v-if="!comment.disabled" class="list-inline-item g-mr-20">
                      <a v-on:click="onClickReply(comment)" class="comment-reply-link u-link-v5 g-color-gray-dark-v4 g-color-primary--hover" href="javascript:;">
                        <i class="icon-note g-pos-rel g-top-1 g-mr-3"></i>
                        回复
                      </a>
                    </li>
                    <ul class="list-inline mb-0 ml-auto">
                      <li style="display: none;" class="list-inline-item g-mr-5">
                        <button v-on:click="onEditComment(comment)" class="btn btn-xs u-btn-outline-purple" data-toggle="modal" data-target="#editCommentModal">编辑</button>
                      </li>
                      <li v-if="!comment.disabled && post.author.id == sharedState.user_id" class="list-inline-item">
                        <button v-on:click="onDisabledComment(comment)" class="btn btn-xs u-btn-outline-purple">屏蔽</button>
                      </li>
                      <li v-if="comment.disabled && post.author.id == sharedState.user_id" class="list-inline-item">
                        <button v-on:click="onEnabledComment(comment)" class="btn btn-xs u-btn-outline-aqua">恢复</button>
                      </li>
                      <li v-if="comment.author.id == sharedState.user_id || post.author.id == sharedState.user_id" class="list-inline-item">
                        <button v-on:click="onDeleteComment(comment)" class="btn btn-xs u-btn-outline-red">删除</button>
                      </li>
                    </ul>
                  </ul>
                </div>
              </div>

              <!--子级评论，按时间正序排列-->
              <div class="g-ml-40 comment-item media g-brd-around g-brd-gray-light-v4 g-pa-30 g-mb-20"
                  v-if="comment.child"
                  v-for="(child, cindex) in comment.child" v-bind:key="cindex"
                  v-bind:id="'c' + child.id">
                <router-link v-bind:to="{ path: `/user/${child.author.id}/` }">
                  <img class="d-flex g-width-50 g-height-50 rounded-circle g-brd-around g-brd-gray-light-v4 g-pa-2 g-mt-3 g-mr-15" v-bind:src="child.author.avatar" v-bind:alt="child.author.name || child.author.username">

                </router-link>
                <div class="media-body">
                  <div class="g-mb-15">
                    <h5 v-if="child.author.id == child.post.author" class="h5 g-color-gray-dark-v1 mb-0"><router-link v-bind:to="{ path: `/user/${child.author.id}/` }" class="comment-author g-text-underline--none--hover">{{ child.author.name || child.author.username }}</router-link> <button class="btn btn-xs u-btn-inset u-btn-outline-red g-mr-5">博文作者</button></h5>
                    <h5 v-else class="h5 g-color-gray-dark-v1 mb-0"><router-link v-bind:to="{ path: `/user/${child.author.id}/` }" class="comment-author g-text-underline--none--hover">{{ child.author.name || child.author.username }}</router-link></h5>
                    <span class="g-color-gray-dark-v4 g-font-size-12">{{ $moment(child.timestamp).format('YYYY年MM月DD日 HH:mm:ss') }}</span>
                  </div>

                  <div v-if="child.disabled" class="g-color-red g-mb-15">此评论包含不良信息，已被禁止显示.</div>
                  <div v-else>
                    <!-- vue-markdown 开始解析markdown，它是子组件，通过 props 给它传值即可
                    v-highlight 是自定义指令，用 highlight.js 语法高亮 -->
                    <vue-markdown
                      :source="child.body"
                      class="markdown-body g-mb-15"
                      v-highlight>
                    </vue-markdown>
                  </div>

                  <ul class="list-inline d-sm-flex my-0">
                    <li v-if="!child.disabled" class="list-inline-item g-mr-20">
                      <a v-on:click="onLikeOrUnlike(child)" class="u-link-v5 g-color-gray-dark-v4 g-color-primary--hover" href="javascript:;">
                        <i v-bind:class="{ 'g-color-red': child.liked.indexOf(parseInt(sharedState.user_id)) != -1 }" class="icon-like g-pos-rel g-top-1 g-mr-3"></i>


                        <span v-if="child.liked.length > 0"> {{ child.liked.length }} 人赞</span>
                        <span v-else>赞</span>
                      </a>
                    </li>
                    <li v-if="!child.disabled" class="list-inline-item g-mr-20">
                      <a v-on:click="onClickReply(child)" class="comment-reply-link u-link-v5 g-color-gray-dark-v4 g-color-primary--hover" href="javascript:;">
                        <i class="icon-note g-pos-rel g-top-1 g-mr-3"></i>
                        回复
                      </a>
                    </li>
                    <ul class="list-inline mb-0 ml-auto">
                      <li style="display: none;" class="list-inline-item g-mr-5">
                        <button v-on:click="onEditComment(child)" class="btn btn-xs u-btn-outline-purple" data-toggle="modal" data-target="#editCommentModal">编辑</button>
                      </li>
                      <li v-if="!child.disabled && post.author.id == sharedState.user_id" class="list-inline-item">
                        <button v-on:click="onDisabledComment(child)" class="btn btn-xs u-btn-outline-purple">屏蔽</button>
                      </li>
                      <li v-if="child.disabled && post.author.id == sharedState.user_id" class="list-inline-item">
                        <button v-on:click="onEnabledComment(child)" class="btn btn-xs u-btn-outline-aqua">恢复</button>
                      </li>
                      <li v-if="child.author.id == sharedState.user_id || post.author.id == sharedState.user_id" class="list-inline-item">
                        <button v-on:click="onDeleteComment(child)" class="btn btn-xs u-btn-outline-red">删除</button>
                      </li>
                    </ul>
                  </ul>
                </div>
              </div>
            </div>

          </div>
          <!-- End Panel Body -->
        </div>


 <!-- Pagination #04 -->
        <div v-if="comments && page_total > 1">
          <pagination
            v-bind:cur-page="page"
            v-bind:per-page="per_page"
            v-bind:total-pages="page_total">
          </pagination>
        </div>
        <!-- End Pagination #04 -->

      <!-- End Articles Content -->
        </div>
<!-- Sidebar -->
      <div class="col-lg-3 g-pt-80">

        <div id="sticker" class="g-mb-50">
          <div id="tocHeader" class="u-heading-v3-1 g-mb-15">
              <h2 class="h5 u-heading-v3__title g-color-primary text-uppercase g-brd-primary">文章目录</h2>
          </div>
          <div id="toc" class="toc"></div>
        </div>

      </div>
      <!-- End Sidebar -->

    </div>

</el-col>
 </el-row>

  </div>
</template>

<script>


  // vue-router 从 Home 页路由到 Post 页后，会重新渲染并且会移除事件，自定义的指令 v-highlight 也不生效了
// 所以，这个页面，在 mounted() 和 updated() 方法中调用 highlightCode() 可以解决代码不高亮问题
import hljs from 'highlight.js'
const highlightCode = () => {
  let blocks = document.querySelectorAll('pre code');
  console.log(blocks)
  Array.prototype.forEach.call(blocks, hljs.highlightBlock);
}

import store from '../store'


// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'




// 评论子组件和分页子组件
import Comment from './Base/Comment'
import Pagination from './Base/Pagination'


// 固定 TOC
import '../assets/jquery.sticky'


export default {
  name: 'Post',
  components: {
    VueMarkdown,
     Comment,
    Pagination
  },
  data() {
    return {
          imgUrl:"http://localhost:8000/api/upload_file/",
        imageSuccessUrl:"",
          dialogImageUrl: '',
        dialogVisible: false,
         classListObj: '', //技术分类 classListObj: '', //技术分类

      page :1,
      per_page: 5,
      count:0,
       page_total:0,
      sharedState: store.state,
      post: {},
       comments: '',
      liker_id:[],
      editForm: {
        title: '',
        summary: '',
           category:'',

        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null,
          categoryError:null,
          summaryError:null,
      },
      showToc: true,

      commentForm: {
        body: '',
        parent_id: '',  // 被回复的评论的 id
        author_id: '',  // 被回复的评论的作者的 id
        author_name: '',  // 被回复的评论的作者的名字
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        bodyError: null
      },
      editCommentForm: {
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        bodyError: null
      }
    }
  },
  computed: {
    btnOutlineColor: function () {
      if (this.sharedState.is_authenticated) {
        if (this.liker_id && this.liker_id.indexOf(parseInt(this.sharedState.user_id)) != -1) {
          return 'u-btn-outline-red'
        } else {
          return 'u-btn-outline-primary'
        }
      } else {
        return 'u-btn-outline-primary'
      }
    }
  },

  methods: {

      imgSuccess(response, file, fileList){
    this.imageSuccessUrl= response.url

    console.log(response.url)
},


       ArtClassData () {


      const path = '/api/posts/classList/'
      this.$axios.get(path)
        .then((response) => {
          // handle success
            this.classListObj = response.data.data

        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)

          // this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },

    getPost (id) {
      const path = `/api/posts/${id}/`
      this.$axios.get(path)
        .then((response) => {
          this.post = response.data

            this.liker_id=[]
//             this.post.liker.forEach((res)=>{
// 	this.liker_id.push({
// 		title: res.id,
// 		});
// })
            for (let i = 0;i<this.post.likers.length;i++){

       this.liker_id.push(this.post.likers[i].id)


     }
  // this.liker_id.splice(index, 1, val);
            console.log("this.liker_id",this.liker_id)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    },
    onEditPost (post) {
      // 不要使用对象引用赋值： this.editForm = post
      // 这样是同一个 post 对象，用户在 editform 中的操作会双向绑定到该 post 上， 你会看到 modal 下面的博客也在变
      // 如果用户修改了一些数据，但是点了 cancel，你就必须在 onResetUpdate() 中重新加载一次博客列表，不然用户会看到修改后但未提交的不对称信息
      this.editForm = Object.assign({}, post)
    },
    onSubmitUpdate () {
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


       if (!this.editForm.summary) {
        this.editForm.errors++
        this.editForm.summaryError = 'Summary is required.'
      } else {
        this.editForm.summaryError = null
      }

         if (!this.editForm.category) {
        this.editForm.errors++
        this.editForm.categoryError = 'Category is required.'
      } else {
        this.editForm.categoryError = null
      }

      if(!this.imageSuccessUrl){
           this.editForm.errors++
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
        body: this.editForm.body,
          category:this.editForm.category,
          image:this.imageSuccessUrl,
      }
      this.$axios.put(path, payload)
        .then((response) => {
          // handle success
          this.getPost(this.editForm.id)
          this.$toasted.success('Successed update the post.', { icon: 'fingerprint' })
          this.editForm.title = '',
          this.editForm.summary = '',
          this.editForm.body = '',
               this.editForm.category = ''
             this.$refs.upload.clearFiles(); // 清除上传图片
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
        })
    },
    onResetUpdate () {
      // 先隐藏 Modal
      $('#updatePostModal').modal('hide')
      // this.getPosts()
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
              if (typeof this.$route.query.redirect == 'undefined') {
                this.$router.push('/')
              } else {
                this.$router.push(this.$route.query.redirect)
              }
            })
            .catch((error) => {
              // handle error
              console.log(error.response.data)
            })

        } else {
          this.$swal('Cancelled', 'The post is safe :)', 'error')
        }
      })
    },

 onLikeOrUnlikePost (post) {
      // 用户需要先登录
      if (!this.sharedState.is_authenticated) {
        this.$toasted.error('您需要先登录才能收藏文章 ...', { icon: 'fingerprint' })
        this.$router.replace({
          path: '/login',
          query: { redirect: this.$route.path + '#like-post' }
        })
      }
      let path = ''
      if (this.liker_id.indexOf(parseInt(this.sharedState.user_id)) != -1) {
        // 当前登录用户已收藏过该文章，再次点击则取消收藏
        path = `/api/posts/${post.id}/unlike/`
      } else {
        path = `/api/posts/${post.id}/like/`
      }
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.getPost(this.$route.params.id)
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },


  getPostComments (id) {

  if (typeof this.$route.query.page != 'undefined') {
        this.page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        this.per_page = this.$route.query.per_page
      }


      const path = `/api/posts/${id}/comments/?page=`+this.page+'&per_page='+this.per_page
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.comments = response.data
          console.log(this.comments)
        this.count=response.data.count
          this.page_total = Math.ceil(this.count/this.per_page)
          //if (response.data._meta.total_items > 0) {
          //  this.comments = response.data
          //}
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onLikeOrUnlike (comment) {
      // 用户需要先登录
      if (!this.sharedState.is_authenticated) {
        this.$toasted.error('您需要先登录才能点赞 ...', { icon: 'fingerprint' })
        this.$router.replace({
          path: '/login',
          query: { redirect: this.$route.path + '#c' + comment.id }
        })
      }

      let path = ''
      if (comment.liked.indexOf(this.sharedState.user_id) != -1) {
        // 当前登录用户已点过赞，再次点击则取消赞
        path = `/api/comments/${comment.id}/like/`
      } else {
        path = `/api/comments/${comment.id}/like/`
      }
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.getPostComments(this.$route.params.id)
          // this.$toasted.success(response.data.message, { icon: 'fingerprint' })
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          // this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },
    onClickReply (comment) {
      // 用户需要先登录
      if (!this.sharedState.is_authenticated) {
        this.$toasted.error('您需要先登录才能回复评论 ...', { icon: 'fingerprint' })
        this.$router.replace({
          path: '/login',
          query: { redirect: this.$route.path + '#c' + comment.id }
        })
      }

      this.commentForm.parent_id = comment.id
      this.commentForm.author_id = comment.author.id
      this.commentForm.author_name = comment.author.name || comment.author.username
    },
    onResetAddComment () {
      this.commentForm.body = ''
      this.commentForm.parent_id = ''
      this.commentForm.author_id = ''
      this.commentForm.author_name = ''
      // 移除错误
      this.commentForm.bodyError = null
      $('#addCommentForm .md-editor').closest('.form-group').removeClass('u-has-error-v1')
      // 评论框回复原位
      $('#addCommentForm').removeClass('g-ml-40')
      $('.card-header').after($('#addCommentForm'))
    },
    onSubmitAddComment (e) {
      this.commentForm.errors = 0  // 重置

      if (!this.commentForm.body) {
        this.commentForm.errors++
        this.commentForm.bodyError = 'Body is required.'
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
        $('#addCommentForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
      } else {
        this.commentForm.bodyError = null
        $('#addCommentForm .md-editor').closest('.form-group').removeClass('u-has-error-v1')
      }

      if (this.commentForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/comments/'
      let payload = ''
      if (this.commentForm.parent_id) {
        // 说明是回复评论
        const at_who = `<a href="/user/${this.commentForm.author_id}" class="g-text-underline--none--hover">回复　${this.commentForm.author_name} </a>`
        payload = {
          body: at_who + this.commentForm.body,
          post: this.$route.params.id,
          parent_id: this.commentForm.parent_id
        }
      } else {
        // 说明是发表一级评论
        payload = {
          body: this.commentForm.body,
          post: this.$route.params.id
        }
      }

      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.getPostComments(this.$route.params.id)
          this.$toasted.success('Successed add a new comment.', { icon: 'fingerprint' })
          this.onResetAddComment()
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },
    onEditComment (comment) {
      // 不要使用对象引用赋值： this.editCommentForm = comment
      // 这样是同一个 comment 对象，用户在 editCommentForm 中的操作会双向绑定到该 comment 上， 你会看到 modal 下面的评论也在变
      // 如果用户修改了一些数据，但是点了 cancel，你就必须在 onResetUpdateComment() 中重新加载一次评论列表，不然用户会看到修改后但未提交的不对称信息
      this.editCommentForm = Object.assign({}, comment)
    },
    onSubmitUpdateComment () {
      this.editCommentForm.errors = 0  // 重置
      // 每次提交前先移除错误，不然错误就会累加
      $('#editCommentForm .form-control-feedback').remove()
      $('#editCommentForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')

      if (!this.editCommentForm.body) {
        this.editCommentForm.errors++
        this.editCommentForm.bodyError = 'Body is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
        $('#editCommentForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editCommentForm .md-editor').after('<small class="form-control-feedback">' + this.editCommentForm.bodyError + '</small>')
      } else {
        this.editCommentForm.bodyError = null
      }

      if (this.editCommentForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      // 先隐藏 Modal
      $('#editCommentModal').modal('hide')

      const path = `/api/comments/${this.editCommentForm.id}`
      const payload = {
        body: this.editCommentForm.body
      }
      this.$axios.put(path, payload)
        .then((response) => {
          // handle success
          this.getPostComments(this.$route.params.id)
          this.$toasted.success('Successed update the comment.', { icon: 'fingerprint' })
          this.editCommentForm.body = ''
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },
    onResetUpdateComment () {
      // 先移除错误
      $('#editCommentForm .form-control-feedback').remove()
      $('#editCommentForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
      // 再隐藏 Modal
      $('#editCommentModal').modal('hide')
      this.$toasted.info('Cancelled, the comment is not update.', { icon: 'fingerprint' })
    },
    onDeleteComment (comment) {
      this.$swal({
        title: "Are you sure?",
        text: "删除操作还会删除该评论的所有子孙评论，建议使用 [屏蔽] 功能仅禁止该评论显示",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!'
      }).then((result) => {
        if(result.value) {
          const path = `/api/comments/${comment.id}/`
          this.$axios.delete(path)
            .then((response) => {
              // handle success
              this.$swal('Deleted', 'You successfully deleted this comment', 'success')
              this.getPostComments(this.$route.params.id)
            })
            .catch((error) => {
              // handle error
              console.log(error.response.data)
              this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
            })
        } else {
          this.$swal('Cancelled', 'The comment is safe :)', 'error')
        }
      })
    },
    onDisabledComment (comment) {
      const path = `/api/comments/${comment.id}/`
      this.$axios.put(path, { "disabled": true })
        .then((response) => {
          // handle success
          this.$swal('Success', 'You successfully disabled this comment', 'success')
          this.getPostComments(this.$route.params.id)
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },
    onEnabledComment (comment) {
      const path = `/api/comments/${comment.id}/`
      this.$axios.put(path, { "disabled": false })
        .then((response) => {
          // handle success
          this.$swal('Success', 'You successfully enabled this comment', 'success')
          this.getPostComments(this.$route.params.id)
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },






    tocAllRight: function (tocHtmlStr) {
      // console.log("toc is parsed :", tocHtmlStr);
      // 必须等 vue-markdown 生成 TOC 之后，再用 jquery 操作 DOM!!!
      // 非默认的列表样式
      $('.toc').find('ul').addClass('u-list-inline');
      // 2、3级目录缩进
      $('.toc ul li ul li').addClass('g-ml-15');
      $('.toc ul li ul li ul li').addClass('g-ml-15');
      // 链接颜色，鼠标悬停颜色
      $('.toc').find('a').addClass('u-link-v5 g-color-aqua g-color-red--hover')
    }
  },
  created () {
    const post_id = this.$route.params.id
      this.ArtClassData()
    this.getPost(post_id)
    this.getPostComments(post_id)
    // 初始化 bootstrap-markdown 编辑器
    $(document).ready(function() {
      $("#editPostFormBody, #commentFormBody, #editCommentFormBody").markdown({
        autofocus:false,
        savable:false,
        iconlibrary: 'fa',  // 使用Font Awesome图标
        language: 'zh'
      })
    })
    // 使用 jquery.sticker.js 插件让 TOC 固定位置
    $(document).ready(function(){
      $("#sticker").sticky({ topSpacing: 10 });
    })
    // tooltip
    $(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip();
    })
    // 点击回复评论链接后，移动并显示评论表单
    $(document).ready(function() {
      $('body').on('click', '.comment-reply-link', function() {
        // 点击回复链接的这个评论
        var $comment = $(this).closest('.comment-item');
        // 把评论框添加到要回复的评论下面
        $comment.after($('#addCommentForm'));
        // 如果是二级评论，评论框要向右缩进
        if ($comment.hasClass('g-ml-40')) {
          $('#addCommentForm').addClass('g-ml-40')
        } else {
          $('#addCommentForm').removeClass('g-ml-40')
        }
        // 光标定位到评论框中
        $('#commentFormBody').focus()
      })
    })
  },

 // 当路由变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
      this.ArtClassData()
    this.getPost(to.params.id)
    this.getPostComments(to.params.id)

    if (to.params.id != from.params.id) {  // 同一篇文章，点击 TOC 跳转到各级标题时，不要清空 TOC
      $('#toc').html('')  // 切换不同文章（点击上/下一篇），如果文章内容没有 markdown 需要解析，则需要先清除上个路由的文章的 TOC，不然会残留下来
    }
  },
  mounted () {
    highlightCode()
       var anchor = document.querySelector("#detail");
            // console.log(anchor,anchor.offsetTop);
            var top = anchor.offsetTop-60;
            document.body.scrollTop = top;
             // Firefox
             document.documentElement.scrollTop = top;
             // Safari
             window.pageYOffset = top;
  },
  updated () {
    highlightCode()
  }
}
</script>
