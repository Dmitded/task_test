<template>
  <v-content>
    <v-container class="my-0 py-0" v-if="loginShow === false">
      <v-layout column align-center class="login">
        <v-card column class="pa-5" width="300">
          <h2 style="font-style: sans-serif;">Вход</h2>
          <v-text-field
            v-model="user.login"
            v-validate="'required'"
            :error-messages="errors.collect('login')"
            data-vv-name="login"
            color="error"
            label="Введите Login"
          ></v-text-field>
          <v-text-field
            v-model="user.password"
            v-validate="'required'"
            :error-messages="errors.collect('password')"
            data-vv-name="password"
            color="error"
            type="password"
            label="Введите пароль"
          ></v-text-field>
          <v-flex pt-3>
            <v-btn color="error" width="100%" @click="login">Войти</v-btn>
          </v-flex>
        </v-card>
      </v-layout>
    </v-container>
    <v-snackbar
      v-model="notification.snackbar"
      :right="notification.x"
      :timeout="notification.timeout"
      :top="notification.y"
      color="error darken-2"
      >
      <v-icon large dark right class="mr-5">block</v-icon>
      Не правильный логин или пароль
      <v-btn
        dark
        text
        @click="notification.snackbar = false"
      >
        Close
      </v-btn>
    </v-snackbar>

    <v-container class="my-0 py-0" v-if="loginShow === true">
      <v-toolbar color="error" dark class="my-3">
        <v-toolbar-title>Панель менеджера</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-toolbar-items>

          <v-text-field
            class="my-auto"
            v-model="search"
            label="Search"
            color="white"
            single-line
            hide-details
            append-icon="search"
          ></v-text-field>
          <v-btn text>Выбор даты</v-btn>
        </v-toolbar-items>

        <v-btn icon @click="logout">
          <v-icon>mdi-exit-to-app</v-icon>
        </v-btn>
      </v-toolbar>
      <v-layout row mx-auto>
        <v-flex lg4>
          <v-data-table
            :headers="headers"
            :items="desserts"
            :sort-by="[]"
            :sort-desc="[false, true]"
            :items-per-page="-1"
            :search="search"
            multi-sort
            class="elevation-1 mb-5"
          >
          <template v-slot:item.status="{ item }">
            <v-chip :color="getColor(item.status)" dark>{{ item.status }}</v-chip>
          </template>
          </v-data-table>
        </v-flex>
        <v-flex lg8>
          <div class="Chart__list">
            <div class="Chart">
              <line-chart></line-chart>
            </div>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
import authAPI from '@/api/user'

export default {
  $_veeValidate: {
    validator: 'new'
  },

  name: 'Home',
  data () {
    return {
      search: '',
      headers: [
        {
          text: 'Рабочий',
          align: 'left',
          value: 'worker'
        },
        { text: 'Килограммов', align: 'center', value: 'payload' },
        { text: 'Статус', align: 'center', value: 'status' }
      ],
      component: [
      ],
      desserts: [
        {
          worker: 'Frozen Yogurt',
          payload: 6.0,
          status: 'Выполнено'
        },
        {
          worker: 'Ice cream sandwich',
          payload: 6.0,
          status: 'В процессе'
        },
        {
          worker: 'Eclair',
          payload: 6.0,
          status: 'Ошибка'
        },
        {
          worker: 'Cupcake',
          payload: 6.0,
          status: 'Выполнено'
        }
      ],
      loginShow: true,
      user: {
        login: '',
        password: ''
      },
      dictionary: {
        custom: {
          login: {
            required: () => 'Поле Login не может быть пустым'
          },
          password: {
            required: () => 'Поле пароля не может быть пустым'
          }
        }
      },
      notification: {
        snackbar: false,
        y: 'top',
        x: 'right',
        timeout: 3000
      }
    }
  },

  mounted () {
    this.$validator.localize('en', this.dictionary)
  },

  methods: {
    getColor (status) {
      if (status === 'Ошибка') return 'red'
      else if (status === 'В процессе') return 'orange'
      else return 'green'
    },
    async login () {
      const valid = await this.$validator.validate()
      if (valid) {
        const resp = await authAPI.login(this.user)
        if (resp === 401) {
          this.notification.snackbar = true
          this.user.login = ''
          this.user.password = ''
        } else {
          await this.$store.dispatch('getData')
          this.user.login = ''
          this.user.password = ''
          this.loginShow = true
        }
      }
    },

    async logout () {
      await this.$store.dispatch('logout')
      this.loginShow = false
    }
  }
}
</script>

<style lang="scss" scoped>
  .login {
    height: 100vh;
    justify-content: center;
  }
</style>
