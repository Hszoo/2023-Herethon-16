from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin


#User = get_user_model()
# 여기서 부터 
class UserManager(BaseUserManager):
    def create_user(self, username, email, name, password=None):
        if not username:
            raise ValueError('must have user name')
        if not email:
            raise ValueError('must have user email')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, name, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            name=name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True #이거 권한까지 줘야 superuser로 admin페이지 접근가능하다... 대박 
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,  PermissionsMixin):
    # 필요한 것 .. 
    # 프로필사진, 한줄소개, 회원가입시 회원이름 저장 
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=10, unique=True)
    #profile = models.ImageField(verbose_name='프로필이미지', blank=True, null=True, upload_to='post_photo')
    #info = models.CharField(max_length=20, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    #is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','name']
    

    def __str__(self):
        return self.username
        
def has_perm(self, perm, obj=None):
    return True

def has_module_perms(self, app_label):
    return True

@property
def is_staff(self):
    return self.is_admin
# 여기까지 custom User 모델 구현 (안되면 삭제하기 )

# class Post(models.Model) :
#     title = models.CharField(verbose_name='제목', max_length=50)
#     # 여행지 필드..
#     duration = models.DurationField(verbose_name='여행기간', null=True)
#     # 여행 동행자 
#     plan = models.TextField(verbose_name='상세일정', null=True)
    
#     # 지도에 표시할 위도 , 경도 
#     latitude = models.CharField(verbose_name='위도', max_length=50, null=True)
#     longitude = models.CharField(verbose_name='경도', max_length=50, null=True)
    
#     record = models.TextField(verbose_name='여행기록', null=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     create_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
#     like_count = models.IntegerField(verbose_name='좋아요개수', null=True)
#     # photo = models.ImageField(verbose_name='이미지', blank=True, null=True, upload_to='post_photo')
#     likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', null=True)
#     def __str__(self): 
#         return self.title

# # 댓글에 해당하는 model 정의 
# class Comment(models.Model) : 
#     comment = models.TextField(max_length=200, null=True, blank=True)
#     date = models.DateTimeField(auto_now_add=True) # 날짜 순으로 댓글 뿌려주기 위해 
#     # post 객체를 참조해서 만들 컬럼 -> target_post 
#     article = models.ForeignKey(Post, on_delete=models.CASCADE) # 게시글 모델 참조 필드 
#     author = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # 게시글 작성자 

#     def __str__(self): 
#         return self.comment