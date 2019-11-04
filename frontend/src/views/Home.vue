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
        <v-toolbar-title class="d-none d-sm-flex">Менеджер {{ NameCurrent }}</v-toolbar-title>

        <v-spacer class="d-none d-sm-flex"></v-spacer>

        <v-toolbar-items>
          <v-text-field
            class="my-auto d-none d-sm-flex"
            v-model="search"
            label="Search"
            color="white"
            single-line
            hide-details
            append-icon="search"
          ></v-text-field>

          <v-menu offset-y>
            <template v-slot:activator="{ on }">
              <v-btn text v-on="on">Выбор даты</v-btn>
            </template>
            <v-date-picker
            class="mt-5"
            v-model="picker"
            color="error"
            :max="maxDate"></v-date-picker>
          </v-menu>
          <v-btn class="d-none d-sm-flex" text @click="dataUpdate(maxDate), picker = maxDate">Обновить данные</v-btn>
          <v-btn class="d-flex d-sm-none" text @click="dataUpdate(maxDate), picker = maxDate">Обновить</v-btn>
        </v-toolbar-items>

        <v-btn icon @click="logout">
          <v-icon>mdi-exit-to-app</v-icon>
        </v-btn>
      </v-toolbar>
      <v-flex justify-space-around row mx-auto flex-row-reverse>
        <v-flex lg8>
          <line-chart :chartData="chartData" :options="options"></line-chart>
        </v-flex>
        <v-flex lg4 mt-8>
          <v-text-field
            class="my-auto d-flex d-sm-none"
            v-model="search"
            label="Search"
            color="white"
            single-line
            hide-details
            append-icon="search"
          ></v-text-field>
          <v-data-table
            :headers="headers"
            :items="workers"
            :sort-by="[]"
            :sort-desc="[false, true]"
            :items-per-page="-1"
            :search="search"
            multi-sort
            class="elevation-1 mb-5"
          >
          </v-data-table>
        </v-flex>
      </v-flex>
    </v-container>
  </v-content>
</template>

<script>
import authAPI from '@/api/user'
import chart from '@/components/Chart.js'

export default {
  $_veeValidate: {
    validator: 'new'
  },

  name: 'Home',
  data () {
    return {
      maxDate: new Date().toISOString().substr(0, 10),
      picker: new Date().toISOString().substr(0, 10),
      search: '',
      headers: [
        {
          text: 'Рабочий',
          align: 'left',
          value: 'worker'
        },
        { text: 'Килограммов', align: 'center', value: 'payload' },
        { text: 'Час', align: 'center', value: 'hour' }
      ],
      component: [
        chart
      ],
      workers: [],
      loginShow: false,
      user: {
        login: '',
        password: ''
      },
      chartData: undefined,
      options: {
        responsive: true,
        maintainAspectRatio: false
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
      NameCurrent: '',
      notification: {
        snackbar: false,
        y: 'top',
        x: 'right',
        timeout: 3000
      }
    }
  },

  watch: {
    picker: function () {
      this.dataUpdate(this.picker)
    }
  },

  mounted () {
    this.$validator.localize('en', this.dictionary)
  },

  created () {
    if (this.$store.state.user.current) {
      let name = this.$store.state.user.current
      this.loginShow = true
      this.NameCurrent = name.name + ' ' + name.middle_name
    }
  },

  methods: {
    async dataUpdate (date) {
      await this.$store.dispatch('getData', date)
      let dataworker = this.$store.state.user.workers.payload_data
      let tempData = []
      dataworker.forEach(function (element) {
        var temp = {}
        temp.hour = element.hour
        temp.payload = element.payload_in_hour
        temp.worker = element.worker_data.name + ' ' + element.worker_data.middle_name + ' ' + element.worker_data.surname
        tempData.push(
          temp
        )
      })
      this.workers = tempData
      this.graphUp()
    },
    async login () {
      const valid = await this.$validator.validate()
      if (valid) {
        const resp = await authAPI.login(this.user)
        if ((resp === 401) || (resp === 403)) {
          this.notification.snackbar = true
          this.user.login = ''
          this.user.password = ''
        } else {
          await this.$store.dispatch('getCurrentUser')
          this.user.login = ''
          this.user.password = ''
          if (this.$store.state.user.current.name) {
            let name = this.$store.state.user.current
            this.loginShow = true
            this.NameCurrent = name.name + ' ' + name.middle_name
            this.dataUpdate()
            this.graphUp()
          }
        }
      }
    },

    async logout () {
      await this.$store.dispatch('logout')
      this.loginShow = false
    },

    graphUp () {
      let dataworker = this.$store.state.user.workers.payload_data
      let datalenght = this.$store.state.user.workers.amount

      let test = []
      let tempid = {
        id: undefined
      }

      let testInt = 1
      let temp = {
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0]
      }

      dataworker.forEach(function (element) {
        var result = ''
        var characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
        var charactersLength = 6

        if (tempid.id === undefined) {
          tempid.id = element.worker_id
          temp.label = element.worker_data.name + ' ' + element.worker_data.middle_name + ' ' + element.worker_data.surname
          temp.data[element.hour - 11] = element.payload_in_hour
          for (var i = 0; i < 6; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength))
          }
          temp.backgroundColor = '#' + result + 'aa'
        } if (datalenght === testInt) {
          tempid.id = element.worker_id
          temp.label = element.worker_data.name + ' ' + element.worker_data.middle_name + ' ' + element.worker_data.surname
          temp.data[element.hour - 11] = element.payload_in_hour
          for (var j = 0; j < 6; j++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength))
          }
          temp.backgroundColor = '#' + result + 'aa'
          test.push(temp)
        } if (tempid.id === element.worker_id) {
          temp.data[element.hour - 11] = element.payload_in_hour
          ++testInt
        } else {
          test.push(temp)
          tempid.id = element.worker_id
          temp = {
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0]
          }
          temp.label = element.worker_data.name + ' ' + element.worker_data.middle_name + ' ' + element.worker_data.surname
          temp.data[element.hour - 11] = element.payload_in_hour
          for (var n = 0; n < 6; n++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength))
          }
          temp.backgroundColor = '#' + result + 'aa'
          ++testInt
        }
      })
      this.chartData = {
        labels: ['11', '12', '13', '14', '15', '16', '17', '18', '19'],
        datasets: test
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
  .graph {
    height: 400px !important;
  }
</style>
