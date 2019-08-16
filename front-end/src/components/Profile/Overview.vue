<template>
  <section>
    <div class="container">
      <div class="g-brd-around g-brd-gray-light-v4 g-pa-20 g-mb-40">
        <div class="row">
          <div class="col-sm-3 g-mb-40 g-mb-0--lg">
            <!-- User Image -->
            <div class="g-mb-20">
              <img v-if="user.avatar" class="img-fluid w-100" v-bind:src="user.avatar" alt="Image Description">
            </div>
            <!-- User Image -->

<!--             Actions-->
<!--            <router-link v-if="$route.params.id == sharedState.user_id" v-bind:to="{ name: 'SettingProfile' }" class="btn btn-block u-btn-outline-primary g-rounded-50 g-py-12 g-mb-10">-->
<!--              <i class="icon-user-follow g-pos-rel g-top-1 g-mr-5"></i> Edit Profile-->
<!--            </router-link>-->
<!--             End Actions -->

          </div>

          <div class="col-sm-9">
            <!-- Username -->
            <div class="d-flex align-items-center justify-content-sm-between g-mb-5">
              <h2 v-if="user.name" class="g-font-weight-300 g-mr-10">{{ user.name }}</h2>
              <h2 v-else class="g-font-weight-300 g-mr-10">{{ user.username }}</h2>
            </div>
            <!-- End Username -->


            <h4 v-if="user.date_joined" class="h6 g-font-weight-300 g-mb-10">
              <i class="icon-badge g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i> Member since : {{ $moment(user.date_joined).format('LLL') }}
            </h4>




            <!-- User Info -->
            <ul class="list-inline g-font-weight-300">
              <li class="list-inline-item g-mr-20">
                <i class="icon-check g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i> 用户信息
              </li>
              <li v-if="user.email" class="list-inline-item g-mr-20">
                <i class="icon-link g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i>  <a class="g-color-main g-color-primary--hover" v-bind:href="'mailto:' + user.email">{{ user.email }}</a>
              </li>
            </ul>
            <!-- End User Info -->

            <!-- Location -->
            <h4 v-if="user.location" class="h6 g-font-weight-300 g-mb-10">
              <i class="icon-location-pin g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i> {{ user.location }}
            </h4>
            <!-- End Location -->

            <div v-if="user.about_me">
              <div class="u-divider u-divider-db-dashed u-divider-center g-brd-gray-light-v2 g-mt-50 g-mb-30">
                <i class="u-divider__icon u-divider__icon--indented g-bg-gray-light-v4 g-color-gray-light-v1 rounded-circle">我</i>
              </div>
             <p class="g-line-height-1_8 g-font-weight-300">{{ user.about_me }}</p>
            </div>


          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import store from '../../store'

export default {
  name: 'Overview',  //this is the name of the component
  data () {
    return {

      sharedState: store.state,
      user: {
        username: '',
        email: '',
        name: '',
        location: '',
        about_me: '',

        date_joined: '',

          self: '',
          avatar: ''

      }
    }
  },
  methods: {
    getUser (id) {
      const path = `/api/users/${id}/`
      this.$axios.get(path)
        .then((response) => {
          this.user = response.data.data
          console.log(this.user)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    }
  },
  created () {
    const user_id = this.$route.params.id
    this.getUser(user_id)
  },
  // 当 id 变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    this.getUser(to.params.id)
    next()
  }
}
</script>
