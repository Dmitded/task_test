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
      loginShow: false,
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
          }// this.$validator.localize('ru', this.dictionary)
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
    async login () {
      const valid = await this.$validator.validate()
      if (valid) {
        const resp = await authAPI.login(this.user)
        if (resp === 401) {
          this.notification.snackbar = true
          this.user.email = ''
          this.user.password = ''
        } else {
          await this.$store.dispatch('getData')
          this.loginShow = true
        }
      }
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
