/**
 * First we will load all of this project's JavaScript dependencies which
 * includes Vue and other libraries.
 */

import Vue from 'vue'
import {Form, HasError, AlertError, AlertErrors, AlertSuccess} from 'vform'
import IMask from 'imask'


require('./bootstrap')
window.Vue = Vue
window.Form = Form
window.IMask = IMask

Vue.component(HasError.name, HasError)
Vue.component(AlertError.name, AlertError)

/**
 * The following block of code may be used to automatically register your
 * Vue components. It will recursively scan this directory for the Vue
 * components and automatically register them with their "basename".
 *
 * Eg. ./components/ExampleComponent.vue -> <example-component></example-component>
 */

const files = require.context('./', true, /\.vue$/i)
files.keys().map(key => Vue.component(key.split('/').pop().split('.')[0], files(key).default))