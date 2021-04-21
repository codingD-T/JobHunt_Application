from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.actionbar import ActionBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem, ThreeLineListItem
from kivymd.uix.list import MDList
from kivy.uix.button import Button
from kivy.lang import Builder
from kivymd.toast import toast
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
import requests
import os



class JobPortal(Widget):
    pass


Login_Page = """
ScreenManager:
    LoginPage
    RegisterPage
    HomePage
    PostJob
    JobDetails
    ApplyPage
    ResumePage
    Description
    ProfilePage
    ApplicationsPage
    UpdateProfilePage
    JobsPage
    ApplicantsPage
    ImagePage
    ResumePageProfile

<UpdateProfilePage>:
    name: "UpdateProfile"
    MDFloatLayout:
        MDLabel:
            text: "Update Profile"
            pos_hint:{"center_y":0.95}
            font_style:"H3"
            halign:"center"
            theme_text_color:"Custom"
            text_color :0,0,0,1
        MDTextField:
            id: dob
            hint_text:"Enter your Date of Birth"
            pos_hint:{"center_x":0.5,"center_y":0.8}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDTextField:
            id: bio
            hint_text:"Enter your Bio"
            pos_hint:{"center_x":0.5,"center_y":0.7}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDTextField:
            id: gender
            hint_text:"Enter your Gender"
            pos_hint:{"center_x":0.5,"center_y":0.6}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8

        MDTextField:
            id: mobile
            hint_text:"Enter your Mobile number"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
            
        MDRaisedButton:
            text:"Update Profile"
            pos_hint:{"center_x":0.5,"center_y":0.15}
            size_hint_x:0.5
            on_release:app.update_profile(dob.text,bio.text,gender.text,mobile.text)
            theme_text_color:"Custom"
            text_color:0,0,0,1
            
    
<ApplicantsPage>:
    name: "Applicants"
    ScrollView:
        MDList:
            
    CustAction:
        pos_hint: {'top':1}
        background_color: 0,0,255,0.5 
        ActionView:
            use_separator: True
            ActionPrevious:
                title: 'Job Hunt'
                icon: 'D:\miniProject\MP\django\JobPortalMobApp\job3.jpg'
                on_press : app.goHome()
            ActionButton:
                text: 'Update Job'
                id: post
                on_press: app.goToPostjob()
            ActionButton:
                text: 'Delete Job'
                on_press: app.deleteJob()


    
<ApplicationsPage>:
    name: "Applications"
    ScrollView:
        MDList:
            
    CustAction:
        pos_hint: {'top':1}
        background_color: 0,0,255,0.5 
        ActionView:
            use_separator: True
            ActionPrevious:
                title: 'Job Hunt'
                icon: 'D:\miniProject\MP\django\JobPortalMobApp\job3.jpg'
                on_press : app.goHome()
            ActionButton:
                text: 'Update Profile'
                id: updateProfile
                on_press: app.goUpdate() 
            ActionButton:
                text: 'Jobs'
                id: post
                on_press: app.goJobs()
            ActionButton:
                text: 'Applications'
                on_press: app.goApplications()
            ActionButton:
                text: 'Delete'
                on_press: app.goDelete()
                
<JobsPage>:
    name: "Jobs"
    ScrollView:
        MDList:
            
    CustAction:
        pos_hint: {'top':1}
        background_color: 0,0,255,0.5 
        ActionView:
            use_separator: True
            ActionPrevious:
                title: 'Job Hunt'
                icon: 'D:\miniProject\MP\django\JobPortalMobApp\job3.jpg'
                on_press : app.goHome()

            ActionButton:
                text: 'Applications'
                on_press: app.goDeleteJob()

    
<ProfilePage>:
    name:"Profile"
    ScrollView:
        MDList:
    CustAction:
        pos_hint: {'top':1}
        background_color: 0,0,255,0.5 
        ActionView:
            use_separator: True
            ActionPrevious:
                title: 'Job Hunt'
                icon: 'D:\miniProject\MP\django\JobPortalMobApp\job3.jpg'
                on_press : app.goHome()
            ActionButton:
                text: 'Update Profile'
                id: updateProfile
                on_press: app.goUpdate() 
            ActionButton:
                text: 'Jobs'
                id: post
                on_press: app.goJobs()
            ActionButton:
                text: 'Applications'
                on_press: app.goApplications()
            ActionButton:
                text: 'Delete'
                on_press: app.goDelete()


<LoginPage>:
    name:"Login"
    MDFloatLayout:
        MDLabel:
            text: "Login"
            pos_hint:{"center_y":0.85}
            font_style:"H3"
            halign:"center"
            theme_text_color:"Custom"
            text_color :0,0,0,1
        MDLabel:
            text: "Welcome to Job Hunt"
            pos_hint:{"center_y":0.75}
            font_style:"H5"
            halign:"center"
            theme_text_color:"Custom"
            text_color :0,0,0,1
        MDTextField:
            id: username
            hint_text:"Enter your Username"
            pos_hint:{"center_x":0.5,"center_y":0.6}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDTextField:
            id: password
            hint_text:"Enter your Password"
            pos_hint:{"center_x":0.5,"center_y":0.45}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
            password:True
        MDRaisedButton:
            text:"Login"
            pos_hint:{"center_x":0.5,"center_y":0.25}
            size_hint_x:0.5
            on_release:app.verify_login(username.text,password.text)
            theme_text_color:"Custom"
            text_color:0,0,0,1
        MDLabel:
            text: "Don't have an account?"
            pos_hint:{"center_x":0.5,"center_y":0.17}
            halign:"center"
            theme_text_color:"Custom"
            text_color :0,0,0,1
        MDTextButton:
            text:"Register"
            pos_hint:{"center_x":0.5,"center_y":0.1}
            text_color :0,1,0,1
            on_press: root.manager.current = "Register"

<RegisterPage>:
    name:"Register"
    MDFloatLayout:
        MDLabel:
            text: "Register"
            pos_hint:{"center_y":0.95}
            font_style:"H3"
            halign:"center"
            theme_text_color:"Custom"
            text_color :0,0,0,1
        MDLabel:
            text: "Welcome to Job Hunt"
            pos_hint:{"center_y":0.85}
            font_style:"H5"
            halign:"center"
            theme_text_color:"Custom"
            text_color :0,0,0,1
        MDTextField:
            id: username
            hint_text:"Enter your Username"
            pos_hint:{"center_x":0.5,"center_y":0.7}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDTextField:
            id: email
            hint_text:"Enter your Email"
            pos_hint:{"center_x":0.5,"center_y":0.55}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDTextField:
            id: password1
            hint_text:"Enter your Password"
            pos_hint:{"center_x":0.5,"center_y":0.4}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
            password:True
        MDTextField:
            id: password2
            hint_text:"Confirm Password"
            pos_hint:{"center_x":0.5,"center_y":0.25}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
            password:True
        MDRaisedButton:
            text:"Register"
            pos_hint:{"center_x":0.5,"center_y":0.15}
            size_hint_x:0.5
            on_release:app.verify_register(username.text,email.text,password1.text,password2.text)
            theme_text_color:"Custom"
            text_color:0,0,0,1
        MDLabel:
            text: "Already have an account?"
            pos_hint:{"center_x":0.5,"center_y":0.08}
            halign:"center"
            theme_text_color:"Custom"
            text_color :0,0,0,1
        MDTextButton:
            text:"Login"
            pos_hint:{"center_x":0.5,"center_y":0.05}
            text_color :0,1,0,1
            on_press: root.manager.current="Login"

<PostJob>:
    name:"PostJob"
    MDFloatLayout:
        MDLabel:
            text: "Post Job"
            pos_hint:{"center_y":0.95}
            font_style:"H3"
            halign:"center"
            theme_text_color:"Custom"
            text_color :0,0,0,1
        MDTextField:
            id: nameOfCompany
            hint_text:"Enter the name of the Company"
            pos_hint:{"center_x":0.5,"center_y":0.8}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDTextField:
            id: position
            hint_text:"Enter the Job Position"
            pos_hint:{"center_x":0.5,"center_y":0.7}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDTextField:
            id: description
            hint_text:"Enter the Job Description"
            pos_hint:{"center_x":0.5,"center_y":0.6}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDTextField:
            id: salary
            hint_text:"Enter the Salary"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDTextField:
            id: exp
            hint_text:"Enter the experience"
            pos_hint:{"center_x":0.5,"center_y":0.4}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDTextField:
            id: loc
            hint_text:"Enter the location"
            pos_hint:{"center_x":0.5,"center_y":0.3}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8

        MDRaisedButton:
            text:"Post"
            pos_hint:{"center_x":0.5,"center_y":0.15}
            size_hint_x:0.5
            on_release:app.post_job(nameOfCompany.text,position.text,description.text,salary.text,exp.text,loc.text)
            theme_text_color:"Custom"
            text_color:0,0,0,1

<Description>:
    name:"Description"

    MDLabel:

        id:describe
        text: ""
        pos_hint:{"center_y":0.75}
        font_style:"H6"
        halign:"center"
        theme_text_color:"Custom"
        text_color :0,0,0,1
    CustAction:
        pos_hint: {'top':1}
        background_color: 0,0,255,0.5 
        ActionView:
            use_separator: True
            ActionPrevious:
                title: 'Job Hunt'
                icon: 'D:\miniProject\MP\django\JobPortalMobApp\job3.jpg'
                on_press : app.goHome()
            ActionButton:
                text: 'Profile'
                on_press: app.goProfile()
            ActionButton:
                text: 'Post'
                id: post
                on_press: app.goPost()
            ActionButton:
                text: 'Logout'
                on_press: app.logout()



<JobDetails>:

    name: "JobDetails"
    ScrollView:
        MDList:
    CustAction:
        pos_hint: {'top':1}
        background_color: 0,0,255,0.5 
        ActionView:
            use_separator: True
            ActionPrevious:
                title: 'Job Hunt'
                icon: 'D:\miniProject\MP\django\JobPortalMobApp\job3.jpg'
                on_press : app.goHome()
            ActionButton:
                text:'Apply'
                on_press:app.gotoApplyPage()
            ActionButton:
                text: 'Profile'
                on_press: app.goProfile()
            ActionButton:
                text: 'Post'
                id: post
                on_press: app.goPost()
            ActionButton:
                text: 'Logout'
                on_press: app.logout()

<HomePage>:
    name:"Home"
    ScrollView:
        MDList:
            id: jobs_list
    CustAction:
        pos_hint: {'top':1}
        background_color: 0,0,255,0.5 
        ActionView:
            use_separator: True
            ActionPrevious:
                title: 'Job Hunt'
                icon: 'D:\miniProject\MP\django\JobPortalMobApp\job3.jpg'
                on_press : app.goHome()
            ActionButton:
                text: 'Profile'
                on_press: app.goProfile()
            ActionButton:
                text: 'Post'
                id: post
                on_press: app.goPost()
            ActionButton:
                text: 'Logout'
                on_press: app.logout()
<ResumePage>:    
    id:file       
    name:"Resume"      
    FileChooserIconView:
        id:filechooser
        canvas.before: 
            Color: 
                rgb: .5, .4, .5
            Rectangle: 
                pos: self.pos 
                size: self.size 
        on_selection: app.selected_file(filechooser.selection)     
        
<ResumePageProfile>:    
    id:file       
    name:"ResumeProfile"      
    FileChooserIconView:
        id:filechooser
        canvas.before: 
            Color: 
                rgb: .5, .4, .5
            Rectangle: 
                pos: self.pos 
                size: self.size 
        on_selection: app.selected_fileProfile(filechooser.selection) 
        
<ImagePage>:    
    id:file       
    name:"Image"      
    FileChooserIconView:
        id:imagechooser
        canvas.before: 
            Color: 
                rgb: .5, .4, .5
            Rectangle: 
                pos: self.pos 
                size: self.size 
        on_selection: app.selected_image(imagechooser.selection)     

<ApplyPage>:
    name:"ApplyPage"
    MDFloatLayout:
        MDLabel:
            text: "Application Form"
            pos_hint:{"center_y":0.85}
            font_style:"H3"
            halign:"center"
            theme_text_color:"Custom"
            text_color :0,0,0,1
        MDTextField:
            id: dob
            hint_text:"Enter your Date of Birth"
            pos_hint:{"center_x":0.5,"center_y":0.7}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDTextField:
            id: gender
            hint_text:"Enter your gender"
            pos_hint:{"center_x":0.5,"center_y":0.55}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDTextField:
            id: mobile
            hint_text:"Enter your Mobile"
            pos_hint:{"center_x":0.5,"center_y":0.4}
            current_hint_text_color:0,0,0,1
            size_hint_x:0.8
        MDRaisedButton:
            text:"Resume"
            pos_hint:{"center_x":0.4,"center_y":0.25}
            size_hint_x:0.5
            on_release: app.goResume()
            text_color:0,0,0,1
        MDRaisedButton:
            text:"Apply"
            pos_hint:{"center_x":0.5,"center_y":0.1}
            size_hint_x:0.5
            on_press: app.gotoApply(dob.text,gender.text,mobile.text)
            theme_text_color:"Custom"
            text_color:0,0,0,1
    CustAction:
        pos_hint: {'top':1}
        background_color: 0,0,255,0.5 
        ActionView:
            use_separator: True
            ActionPrevious:
                title: 'Job Hunt'
                icon: 'D:\miniProject\MP\django\JobPortalMobApp\job3.jpg'
                on_press : app.goHome()
            ActionButton:
                text: 'Profile'
                on_press: app.goProfile()
            ActionButton:
                text: 'Post'
                id: post
                on_press: app.goPost()
            ActionButton:
                text: 'Logout'
                on_press: app.logout()



"""

class ApplicantsPage(Screen):
    pass

class JobsPage(Screen):
    pass

class UpdateProfilePage(Screen):
    pass

class ResumePage(Screen):
    def select(self, *args):
            self.label.text = args[1][0]
            print(self.label.text)


class CustAction(ActionBar):
    pass

class ProfilePage(Screen):
    pass

class LoginPage(Screen):
    pass


class RegisterPage(Screen):
    pass


class HomePage(Screen):
    pass


class PostJob(Screen):
    pass


class JobDetails(Screen):
    pass

class ResumePageProfile(Screen):
    pass


class ApplyPage(Screen):
    pass


class Description(Screen):
    pass

class ApplicationsPage(Screen):
    pass

class ImagePage(Screen):
    pass

sm = ScreenManager()
sm.add_widget(LoginPage(name="Login"))
sm.add_widget(RegisterPage(name="Register"))
sm.add_widget(HomePage(name="Home"))
sm.add_widget(PostJob(name="PostJob"))
sm.add_widget(JobDetails(name="JobDetails"))
sm.add_widget(ApplyPage(name="ApplyPage"))
sm.add_widget(ResumePage(name="Resume"))
sm.add_widget(Description(name="Description"))
sm.add_widget(ProfilePage(name="Profile"))
sm.add_widget(ApplicationsPage(name="Applications"))
sm.add_widget(UpdateProfilePage(name="UpdateProfile"))
sm.add_widget(JobsPage(name="Jobs"))
sm.add_widget(ApplicantsPage(name="Applicants"))
sm.add_widget(ImagePage(name="Image"))
sm.add_widget(ResumePageProfile(name="ResumeProfile"))

class OneLineListItemAligned(OneLineListItem):
    def __init__(self, halign, **kwargs):
        super(OneLineListItemAligned, self).__init__(**kwargs)
        self.ids._lbl_primary.halign = halign


class MainJobPortal(MDApp):

    def __iter__(self):
        super(MainJobPortal, self).__init__()
        self.home_text = ""

    class ContentNavigationDrawer(BoxLayout):
        pass

    class DrawerList(ThemableBehavior, MDList):
        pass

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        login_page = Builder.load_string(Login_Page)

        return login_page

    def verify_login(self, username, password):
        print("Hello Login")
        login_info = {
            "username": username,
            "password": password
        }

        url_login = "https://jobhunt-disha-tushar.herokuapp.com/api/login/"
        response = requests.post(url_login, data=login_info)
        url_auth = "https://jobhunt-disha-tushar.herokuapp.com/api/auth/"
        self.header_token = requests.post(url_auth, data=login_info)
        self.header = {'Authorization': f'Token {self.header_token.json()}'}
        print(response)
        print(self.header)
        if response.ok:
            self.root.current = "Home"
            self.getText()
        else:
            toast("Invalid credentials")

    def on_start(self):
        pass

    def verify_register(self, u, e, p1, p2):
        print("Hello Register")
        toast("User created")
        register_info = {
            "username": u,
            "email": e,
            "password": p1,
            "password2": p2
        }

        url = "https://jobhunt-disha-tushar.herokuapp.com/api/register/"
        response = requests.post(url, data=register_info)
        print(response)
        if response.ok:
            self.root.current = "Login"
            toast("User created")
        else:
            toast(response)

    def post_job(self, n, p, d, s, e, l):
        job_info = {"name": n,
                    "position": p,
                    "description": d,
                    "salary": s,
                    "experience": e,
                    "Location": l}
        url_post = "https://jobhunt-disha-tushar.herokuapp.com/api/postjob/"
        response = requests.post(url_post, headers=self.header, data=job_info)
        print(response)
        if response.ok:
            self.root.current = "Home"
            toast("Job Posted")
        else:
            toast("Job not posted. Please try again")
            self.root.current = "Home"

    def goPost(self):
        print('heyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
        self.root.current = "PostJob"

    def logout(self):
        url_log = "https://jobhunt-disha-tushar.herokuapp.com/api/logout/"
        response = requests.post(url_log, headers=self.header)
        print(response)
        if response.ok:
            self.root.current = "Login"
            toast("Logged out Succesfully")
        else:
            toast("Cannot Log out")

    def getText(self):
        url_home = "https://jobhunt-disha-tushar.herokuapp.com/api/home/"
        print(self.header)
        response = requests.get(url_home, headers=self.header)
        print(response)
        print(sm.ids)
        if response.ok:
            # self.root.get_screen('widgets').ids.lololo.text = 'changed'
            print(self.root.get_screen('Home').ids['jobs_list'])
            scroll = ScrollView(size_hint=(1, 0.91), )
            list_view = MDList()
            scroll.add_widget(list_view)
            for i in response.json():
                print("Companies", i)
                one = OneLineListItem(
                    text="Company id: " + str(i["id"]) + '    Company name: ' + i["name"] + '    Job position: ' + i[
                        "position"], on_release=self.pass_id)
                list_view.add_widget(one)
            self.root.get_screen('Home').add_widget(scroll)

        else:
            toast("Network issues. Please try again later after building your profile")

    #
    def pass_id(self, onelinelistitem):
        x = onelinelistitem.text.split()[2]
        print(x)
        self.company_id = int(x)
        url_home = "https://jobhunt-disha-tushar.herokuapp.com/api/home/"
        print(self.header)
        response = requests.get(url_home, headers=self.header)
        print(response)
        for i in response.json():
            print(i["id"], int(x))
            if i["id"] == int(x):

                self.root.current = "JobDetails"

                scroll = ScrollView(size_hint=(1, 0.91), )
                list_view = MDList()
                scroll.add_widget(list_view)
                for j in i.keys():
                    if j == "id":
                        continue
                    if j == "description":
                        one = OneLineListItem(on_press=self.describe, text=str(j))
                        list_view.add_widget(one)
                    else:
                        one = OneLineListItem(text=str(j) + ": " + str(i[j]))
                        list_view.add_widget(one)
                self.root.get_screen('JobDetails').add_widget(scroll)

                # self.root.get_screen('JobDetails').ids['jobdescribe'].on_press=self.describe()'''
                # self.root.get_screen('JobDetails').add_widget(Button(text="Description",on_press=self.describe))

                '''
                self.root.get_screen('JobDetails').ids['companyName'].text ="Company name: "+ i["name"]
                self.root.get_screen('JobDetails').ids['position'].text  = "Position: "+i["position"]
                self.root.get_screen('JobDetails').ids['salary'].text  = "Salary: "+str(i["salary"])
                self.root.get_screen('JobDetails').ids['description'].text  = "Description: "+i["description"]
                self.root.get_screen('JobDetails').ids['exp'].text  = "Experience: "+str(i["experience"])
                self.root.get_screen('JobDetails').ids['Location'].text  = "Location: "+i["Location"]'''

    def gotoApply(self,dob,gender,mobile):
        job_info = {"dob": dob,
                    "gender": gender,
                    "mobile": mobile,
                    "resume": self.filename,
                    }
        header = {'Authorization': f'Token {self.header_token.json()}', "Content-Type": "/",
                  'Content-Disposition': 'attachment; filename=file',
                  'filename': 'file'}
        self.root.current = "ApplyPage"
        url_apply_base = "https://jobhunt-disha-tushar.herokuapp.com/api/applyjob/" + str(self.company_id) + '/'
        print(url_apply_base)
        print(self.filename)
        response = requests.post(url_apply_base,headers=header,data=job_info)
        print(response)
        if response.ok:
            toast("You applied for this job")
            self.root.current = "Home"

    def goResume(self):
        self.root.current = "Resume"

    def goImage(self):
        self.root.current = "Image"

    def describe(self, text):
        self.root.current = "Description"
        url_home = "https://jobhunt-disha-tushar.herokuapp.com/api/home/"
        print(self.header)
        response = requests.get(url_home, headers=self.header)
        print(response)
        for i in response.json():
            print(i)
            if i["id"] == self.company_id:
                self.root.get_screen('Description').ids['describe'].text = "Description: " + i['description']

    def goProfile(self):
        self.root.current = "Profile"
        scroll = ScrollView(size_hint=(1, 0.91))
        list_view = MDList()
        scroll.add_widget(list_view)
        response = requests.get("https://jobhunt-disha-tushar.herokuapp.com/api/giveProfile/",headers=self.header)
        print(response,type(response.json()[0]))
        for i,j in response.json()[0].items():
            if i == "id":
                continue
            print("Companies", i)
            one = OneLineListItem(text=str(i) + "    " + str(j))
            list_view.add_widget(one)
        self.root.get_screen('Profile').add_widget(scroll)

    def getId(self,text):
        text = text.text.split()[0]
        print(text)
        self.goApplicants(text)

    def goJobs(self):
        response = requests.get("https://jobhunt-disha-tushar.herokuapp.com/api/jobs/", headers=self.header)
        print(response)
        if response.ok:
            self.root.current = "Jobs"
            scroll = ScrollView(size_hint=(1, 0.91))
            list_view = MDList()
            scroll.add_widget(list_view)
            for i in response.json():
                print("Jobs", i)
                one = OneLineListItem(text=str(i["id"]) + '    Company name: ' + i["name"],on_press=self.getId )
                list_view.add_widget(one)
            self.root.get_screen('Jobs').add_widget(scroll)

    def goApplicants(self,text):

        url_base = "https://jobhunt-disha-tushar.herokuapp.com/api/applicants/" + text
        response = requests.get(url_base, headers=self.header)
        print(text,response)
        print(response)
        if response.ok:
            self.root.current = "Applicants"
            scroll = ScrollView(size_hint=(1, 0.91))
            list_view = MDList()
            scroll.add_widget(list_view)
            for i in response.json():
                print("Jobs", i)
                one = OneLineListItem(text='Applicant name: ' + str(i['name']))
                list_view.add_widget(one)
            self.root.get_screen('Applicants').add_widget(scroll)

    def goApplications(self):
        response = requests.get("https://jobhunt-disha-tushar.herokuapp.com/api/applications/", headers=self.header)
        print(response)
        if response.ok:
            self.root.current = "Applications"
            scroll = ScrollView(size_hint=(1, 0.91))
            list_view = MDList()
            scroll.add_widget(list_view)
            for i in response.json():
                print("Companies", i)
                one = OneLineListItem(text="Company id: " + str(i["id"]) + '    Company name: ' + i["name"])
                list_view.add_widget(one)
            self.root.get_screen('Applications').add_widget(scroll)

    def selected_file(self,filename):
        text = filename[0]
        print(len(text))
        if len(text) == 0:
            self.filename = ""
        else:
            self.filename = text
        self.root.current = "ApplyPage"

    def selected_fileProfile(self,filename):
        text = filename[0]
        print(len(text))
        if len(text) == 0:
            self.filename = ""
        else:
            self.filename = text
        self.root.current = "UpdateProfile"

    def selected_image(self,filename):
        text = filename[0]
        print(len(text))
        if len(text) == 0:
            self.image = ""
        else:
            self.image = text
        self.root.current = "UpdateProfile"

    def update_profile(self,dob,bio,gender,mobile):
        job_info = {"dob": dob,
                    "bio":bio,
                    "gender": gender,
                    "mobile": mobile,
                    "resume": '',
                    }
        print(job_info)
        header = {'Authorization': f'Token {self.header_token.json()}'}
        profile = requests.post("https://jobhunt-disha-tushar.herokuapp.com/api/updateprofile/", headers=header, data=job_info)
        print(profile)
        if profile.ok:
            self.root.current = "Profile"
            toast("Profile updated successfully")

    def gotoApplyPage(self):
        self.root.current = "ApplyPage"

    def goUpdate(self):
        self.root.current = "UpdateProfile"

    def updateResume(self):
        self.root.current = "ResumeProfile"

    def goHome(self):
        self.root.current = "Home"

    def goToPostjob(self):
        self.root.current = "PostJob"

if __name__ == "__main__":
    MainJobPortal().run()
