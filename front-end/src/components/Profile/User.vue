<template>
  <section>


<!-- Modal: Send Messages -->
    <div data-backdrop="static" class="modal fade" id="sendMessagesModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">群发私信</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">

            <form id="sendMessagesForm" @submit.prevent="onSubmitSendMessages" @reset.prevent="onResetSendMessages">
              <div class="form-group">
                <textarea v-model="sendMessagesForm.body" class="form-control" id="sendMessagesFormBody" rows="5" placeholder=" 内容"></textarea>
                <small class="form-control-feedback" v-show="sendMessagesForm.bodyError">{{ sendMessagesForm.bodyError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Send</button>
            </form>

          </div>
        </div>
      </div>
    </div>
    <!-- End Modal: Send Messages -->


    <!-- 用户信息 -->
    <div v-if="user" class="container">
      <div class="g-brd-around g-brd-gray-light-v4 g-pa-20 g-mb-40">
        <div class="row">
          <div class="col-sm-3 g-mb-40 g-mb-0--lg">
            <!-- User Image -->
            <div class="g-mb-20">

<!--           <img v-if="user.avatar" class="img-fluid w-100" v-bind:src="user.avatar" v-bind:alt="user.name || user.username">-->

            </div>
            <!-- User Image -->

            <!-- Actions -->


            <button v-if="!is_following && $route.params.id != sharedState.user_id" v-on:click="onFollowUser($route.params.id)" class="btn btn-block u-btn-outline-primary g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-user-follow g-pos-rel g-top-1 g-mr-5"></i> 关注
            </button>

            <button v-if="is_following && $route.params.id != sharedState.user_id" v-on:click="onUnfollowUser($route.params.id)" class="btn btn-block u-btn-outline-red g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-user-unfollow g-pos-rel g-top-1 g-mr-5"></i> 取消关注
            </button>


            <router-link v-if="$route.params.id != sharedState.user_id" v-bind:to="{ name: 'MessagesHistoryResource', query: { from: $route.params.id } }" class="btn btn-block u-btn-outline-purple g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-bubble g-pos-rel g-top-1 g-mr-5"></i> 发私信
            </router-link>





            <router-link v-if="$route.params.id == sharedState.user_id" v-bind:to="{ name: 'SettingProfile' }" class="btn btn-block u-btn-outline-primary g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-settings g-pos-rel g-top-1 g-mr-5"></i> 设置
            </router-link>


             <button v-if="sharedState.user_perms=='true'  &&  $route.params.id == sharedState.user_id" data-toggle="modal" data-target="#sendMessagesModal" class="btn btn-block u-btn-outline-aqua g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-bubble g-pos-rel g-top-1 g-mr-5"></i> 群发私信
            </button>

            <!-- End Actions -->

          </div>

          <div class="col-sm-9">

            <!-- Tab Nav -->
            <ul class="nav nav-tabs g-mb-20">
              <li class="nav-item">
                <router-link v-bind:to="{ name: 'UserOverview' }" v-bind:active-class="'active'" class="nav-link" v-bind:class="isUserOverView">我的信息 <span class="u-label g-font-size-11 g-bg-primary g-rounded-20 g-px-10"><i class="icon-layers g-pos-rel g-top-1 g-mr-8"></i></span></router-link>
              </li>


              <li class="nav-item">
                <router-link v-bind:to="{ name: 'UserFollowers' }" v-bind:active-class="'active'" class="nav-link">粉丝 <span class="u-label g-font-size-11 g-bg-deeporange g-rounded-20 g-px-10">{{ user.followers_count }}</span></router-link>
              </li>
              <li class="nav-item">
                <router-link v-bind:to="{ name: 'UserFollowing' }" v-bind:active-class="'active'" class="nav-link">关注 <span class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10">{{ user.followeds_count }}</span></router-link>
              </li>
              <li class="nav-item">
                <router-link v-bind:to="{ name: 'UserPosts' }" v-bind:active-class="'active'" class="nav-link" v-bind:class="{'active': $route.name == 'UserFollowingPosts'}">文章 <span class="u-label g-font-size-11 g-bg-purple g-rounded-20 g-px-10">{{ user.posts_count }}</span></router-link>
              </li>

            </ul>

            <!-- 嵌套的子路由出口 -->
            <router-view></router-view>

          </div>
        </div>
      </div>
    </div>


  </section>
</template>

<script>

import store from '../../store'
// bootstrap-markdown 编辑器依赖的 JS 文件，初始化编辑器在组件的 created() 方法中，同时它需要 JQuery 支持哦
import '../../assets/bootstrap-markdown/js/bootstrap-markdown.js'
import '../../assets/bootstrap-markdown/js/bootstrap-markdown.zh.js'
import '../../assets/bootstrap-markdown/js/marked.js'


export default {
  name: 'User',  //this is the name of the component

  data () {
    return {
      sharedState: store.state,
      user: '',
      is_following:true,
      postForm: {
        title: '',
        summary: '',
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null

      },
         sendMessagesForm: {
        body: '',
        bodyError: null
      },
    }
  },
  computed: {
    isUserOverView: function () {
        // const tabs = ['UserFollowers', 'UserFollowing', 'UserPostsList', 'UserFollowedsPostsList', 'UserCommentsList']
      const tabs = ['UserFollowers', 'UserFollowing', 'UserPosts', 'UserFollowingPosts']
      if (tabs.indexOf(this.$route.name) == -1) {
        return 'active'
      } else {
        return ''
      }
    }
  },
  methods: {
    getUser (id) {
      const path = `/api/users/${id}/`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          // TODO USER
          this.user = response.data.data
          this.is_following = response.data.is_following

        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onFollowUser (id) {
      const path = `/api/follow/${id}/`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.getUser(id)
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onUnfollowUser (id) {
      const path = `/api/unfollow/${id}/`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.getUser(id)

        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },




  },
  created () {
    const user_id = this.$route.params.id
    this.getUser(user_id)


  },
  // 当 id 变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    this.getUser(to.params.id)


  }
}
</script>
