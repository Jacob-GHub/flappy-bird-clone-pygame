import pygame
from sys import exit
from random import randint, choice

#gameinfo
pygame.init()
screen = pygame.display.set_mode((506, 512))
pygame.display.set_caption('FlappyBird')
clock = pygame.time.Clock()
flappy_font = pygame.font.Font('font/flappy-font.ttf', 50)
flappy_font1 = pygame.font.Font('font/flappy-font.ttf', 30)
startover=False
temp_score=0

game_active=False
game_start=True
#background graphics
background_surface=pygame.image.load('graphics/background-day.png').convert()
base_surface=pygame.image.load('graphics/base.png').convert()
base_surface_scaled = pygame.transform.scale(base_surface, (600,150))
base_x_position=0
base_x_position_2=512
#pygame.mixer.init(44100, -16, 2, 2048)

#numbergraphics
zero_surface=pygame.image.load('graphics/0.png').convert_alpha()
one_surface=pygame.image.load('graphics/1.png').convert_alpha()
two_surface=pygame.image.load('graphics/2.png').convert_alpha()
three_surface=pygame.image.load('graphics/3.png').convert_alpha()
four_surface=pygame.image.load('graphics/4.png').convert_alpha()
five_surface=pygame.image.load('graphics/5.png').convert_alpha()
six_surface=pygame.image.load('graphics/6.png').convert_alpha()
seven_surface=pygame.image.load('graphics/7.png').convert_alpha()
eight_surface=pygame.image.load('graphics/8.png').convert_alpha()
nine_surface=pygame.image.load('graphics/9.png').convert_alpha()

get_ready_x_pos=253
get_ready_y_pos=256

game_over_message=pygame.image.load('graphics/gameover.png').convert_alpha()
game_over_message=pygame.transform.rotozoom(game_over_message,0,1.2)
game_over_message_rect=game_over_message.get_rect(center=(253,50))

point=pygame.mixer.Sound('audio/point.wav')
swoosh=pygame.mixer.Sound('audio/swoosh.wav')
bird_jump=pygame.mixer.Sound('audio/wing2.wav')
point.set_volume(0.1)
bird_jump.set_volume(.12)

#playerclass/birdclass
class Player(pygame.sprite.Sprite):
	def __init__(self,x,y):
		super().__init__()
		#different bird graphics
		blue_bird_texture_1 = pygame.image.load('graphics/yellowbird-downflap.png').convert_alpha()
		blue_bird_texture_2 = pygame.image.load('graphics/yellowbird-midflap.png').convert_alpha()
		blue_bird_texture_3 = pygame.image.load('graphics/yellowbird-upflap.png').convert_alpha()

		bird_texture_1_scaled = pygame.transform.scale(blue_bird_texture_1, (50,40)).convert_alpha()
		bird_texture_2_scaled = pygame.transform.scale(blue_bird_texture_2, (50,40)).convert_alpha()
		bird_texture_3_scaled = pygame.transform.scale(blue_bird_texture_3, (50,40)).convert_alpha()

		#sounds
		self.bird_jump=pygame.mixer.Sound('audio/wing2.wav')
		self.bird_jump.set_volume(.12)
		self.fall_sound=pygame.mixer.Sound('audio/die.wav')
		self.hit_sound=pygame.mixer.Sound('audio/hit.wav')
		self.hit_sound.set_volume(0.1)
		self.swoosh=pygame.mixer.Sound('audio/swoosh.wav')
		self.channel = pygame.mixer.Channel(0)

		self.bird_flap = [bird_texture_1_scaled,bird_texture_2_scaled,bird_texture_3_scaled]
		self.flap_index = 1

		self.image = self.bird_flap[self.flap_index]
		self.rect = self.image.get_rect()
		#midbottom = (80,256)
		self.x=x
		self.y=y
		self.rect.midbottom=(x,y)
		self.gravity = 0
		self.random_rotate=randint(0,360)
		

	def player_animation(self):
			if self.gravity<0:
				self.flap_index += 0.2
				if self.flap_index >= len(self.bird_flap):self.flap_index = 0
				self.image = self.bird_flap[int(self.flap_index)]
				self.image=pygame.transform.rotate(self.image,45)
			else: 
				if game_active==False and startover==True:
					self.image=self.bird_flap[1]
					self.image=pygame.transform.rotate(self.image,self.random_rotate)
				else:
					self.flap_index += 0.2
					if self.flap_index >= len(self.bird_flap):self.flap_index = 0
					self.image = self.bird_flap[int(self.flap_index)]
	
	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			self.gravity = -5
			#self.channel.play(self.bird_jump)

		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			self.gravity = -5
			self.channel.play(self.bird_jump)

	def apply_gravity(self):
		if game_active==True or startover==True:
			self.gravity += .35
			self.rect.y += self.gravity
			self.y+=self.gravity
			if self.rect.bottom >= 450:
				self.rect.bottom = 450

	def hit_object(self,fall):
		if(fall):
			self.hit_sound.play()
			self.fall_sound.play()
			self.gravity=5
			self.rect.y += self.gravity
			self.y+=self.gravity
			if self.rect.bottom >= 450:
				self.rect.bottom = 450
				self.swoosh.play()
				

	def update(self):
		self.player_input()
		self.player_animation()
		self.apply_gravity()
		self.hit_object(False)	
	



class Pipe(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		pipe=pygame.image.load('graphics/pipe-green.png').convert_alpha()
		self.image=pipe
		global pipe_y_position
		pipe_y_position=randint(500,750)
		self.rect = self.image.get_rect(midbottom = (600,pipe_y_position))
		self.x=600

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()
	
	def update(self):
		self.rect.x -= 3
		self.x-=3
		self.destroy()

class SkyPipe(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		skypipe=pygame.image.load('graphics/pipe-green.png').convert_alpha()
		skypipe_flipped = pygame.transform.flip(skypipe, False, True) 
		self.image=skypipe_flipped
		global sky_pipe_y_position
		sky_pipe_y_position=pipe_y_position-470
		self.rect = self.image.get_rect(midbottom = (600,sky_pipe_y_position))
	
	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()
	
	def update(self):
		self.rect.x -= 3
		self.destroy()
		

player = pygame.sprite.GroupSingle()
player.add(Player(80,256))
pipe_group = pygame.sprite.Group()
skypipe_group = pygame.sprite.Group()



#collision function
def collision_sprite():
	if (pygame.sprite.spritecollide(player.sprite,pipe_group,False)) or (pygame.sprite.spritecollide(player.sprite,skypipe_group,False)) or(player.sprite.rect.y<-300)or(player.sprite.rect.y==410):
		fall=True
		player.sprite.hit_object(fall)
		return False
	else: return True


score=0
def score_function(score):
	for p in pipe_group:

		#print(p.x)
		#print(player.sprite.x)
		if p.x==player.sprite.x+1:
			return 1
	return 0	
	
def score_surface(score):
	if(score<10):
		if(score==1):
			screen.blit(one_surface,(253,30))
		elif(score==2):
			screen.blit(two_surface,(253,30))
		elif(score==3):
			screen.blit(three_surface,(253,30))
		elif(score==4):
			screen.blit(four_surface,(253,30))
		elif(score==5):
			screen.blit(five_surface,(253,30))
		elif(score==6):
			screen.blit(six_surface,(253,30))
		elif(score==7):
			screen.blit(seven_surface,(253,30))
		elif(score==8):
			screen.blit(eight_surface,(253,30))
		elif(score==9):
			screen.blit(nine_surface,(253,30))
		elif(score==0):
			screen.blit(zero_surface,(253,30))
	elif(score<100 and score>9):
		if(score%10==1):
			screen.blit(one_surface,(265,30))
		elif(score%10==2):
			screen.blit(two_surface,(265,30))
		elif(score%10==3):
			screen.blit(three_surface,(265,30))
		elif(score%10==4):
			screen.blit(four_surface,(265,30))
		elif(score%10==5):
			screen.blit(five_surface,(265,30))
		elif(score%10==6):
			screen.blit(six_surface,(265,30))
		elif(score%10==7):
			screen.blit(seven_surface,(265,30))
		elif(score%10==8):
			screen.blit(eight_surface,(265,30))
		elif(score%10==9):
			screen.blit(nine_surface,(265,30))
		elif(score%10==0):
			screen.blit(zero_surface,(265,30))

		if(int(score/10)==1):
			screen.blit(one_surface,(250,30))
		elif(int(score/10)==2):
			screen.blit(two_surface,(241,30))
		elif(int(score/10)==3):
			screen.blit(three_surface,(241,30))
		elif(int(score/10)==4):
			screen.blit(four_surface,(241,30))
		elif(int(score/10)==5):
			screen.blit(five_surface,(241,30))
		elif(int(score/10)==6):
			screen.blit(six_surface,(241,30))
		elif(int(score/10)==7):
			screen.blit(seven_surface,(241,30))
		elif(int(score/10)==8):
			screen.blit(eight_surface,(241,30))
		elif(int(score/10)==9):
			screen.blit(nine_surface,(241,30))
		elif(int(score/10)==0):
			screen.blit(zero_surface,(241,30))
	elif (score<1000 and score>99):
		if(score%10==1):
			screen.blit(one_surface,(277,30))
		elif(score%10==2):
			screen.blit(two_surface,(277,30))
		elif(score%10==3):
			screen.blit(three_surface,(277,30))
		elif(score%10==4):
			screen.blit(four_surface,(277,30))
		elif(score%10==5):
			screen.blit(five_surface,(277,30))
		elif(score%10==6):
			screen.blit(six_surface,(277,30))
		elif(score%10==7):
			screen.blit(seven_surface,(277,30))
		elif(score%10==8):
			screen.blit(eight_surface,(277,30))
		elif(score%10==9):
			screen.blit(nine_surface,(277,30))
		elif(score%10==0):
			screen.blit(zero_surface,(277,30))

		if(int((score%100)/100)==1):
			screen.blit(one_surface,(253,30))
		elif(int((score%100)/100)==2):
			screen.blit(two_surface,(253,30))
		elif(int((score%100)/100)==3):
			screen.blit(three_surface,(253,30))
		elif(int((score%100)/100)==4):
			screen.blit(four_surface,(253,30))
		elif(int((score%100)/100)==5):
			screen.blit(five_surface,(253,30))
		elif(int((score%100)/100)==6):
			screen.blit(six_surface,(253,30))
		elif(int((score%100)/100)==7):
			screen.blit(seven_surface,(253,30))
		elif(int((score%100)/100)==8):
			screen.blit(eight_surface,(253,30))
		elif(int((score%100)/100)==9):
			screen.blit(nine_surface,(253,30))
		elif(int((score%100)/100)==0):
			screen.blit(zero_surface,(253,30))


		if(int(score/100)==1):
			screen.blit(one_surface,(235,30))
		elif(int(score/100)==2):
			screen.blit(two_surface,(229,30))
		elif(int(score/100)==3):
			screen.blit(three_surface,(229,30))
		elif(int(score/100)==4):
			screen.blit(four_surface,(229,30))
		elif(int(score/100)==5):
			screen.blit(five_surface,(229,30))
		elif(int(score/100)==6):
			screen.blit(six_surface,(229,30))
		elif(int(score/100)==7):
			screen.blit(seven_surface,(229,30))
		elif(int(score/100)==8):
			screen.blit(eight_surface,(229,30))
		elif(int(score/100)==9):
			screen.blit(nine_surface,(229,30))
		elif(int(score/100)==0):
			screen.blit(zero_surface,(229,30))
	elif (score >=999):
		screen.blit(nine_surface,(277,30))
		screen.blit(nine_surface,(253,30))
		screen.blit(nine_surface,(229,30))
currScore=0
def save_score(param):
	global currScore
	if(param!=0):
		currScore=param

#obstacletimer
pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer,1500)
player_y_position=0

#gameloop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if game_active:
			if event.type == pipe_timer:
				pipe_group.add(Pipe())
				skypipe_group.add(SkyPipe())
		else:
			if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and startover==False)or(event.type == pygame.MOUSEBUTTONDOWN and startover==False):
				game_active = True
			if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and startover==True)or(event.type == pygame.MOUSEBUTTONDOWN and startover==True):
				startover = False
				game_active=False
				player.sprite.rect.bottom=256
				swoosh.play()

	if game_active==True:
		screen.blit(background_surface,(0,0))
		screen.blit(background_surface,(288,0))
		base_x_position-=4

		pipe_group.draw(screen)
		skypipe_group.draw(screen)
		player.draw(screen)
	
		player.update()	
		pipe_group.update()
		skypipe_group.update()
		#score_counter()

		game_active = collision_sprite()
		channel = pygame.mixer.Channel(1)
		score+=score_function(score)
		if(score_function(score)):
			channel.play(point)
		score_surface(score)

		channel2 = pygame.mixer.Channel(2)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			channel2.play(bird_jump)
	 
		
		if base_x_position <-600:
			base_x_position=500
		screen.blit(base_surface_scaled,(base_x_position,450))

		base_x_position_2-=4
		if base_x_position_2 <-600:
			base_x_position_2=500
		screen.blit(base_surface_scaled,(base_x_position_2,450))


			
		#pipe.draw(screen)
		#player.update()
	elif game_active==False:
			screen.blit(background_surface,(0,0))
			screen.blit(background_surface,(288,0))
			pipe_group.draw(screen)
			skypipe_group.draw(screen)
			player.draw(screen)
			player.update()
			base_x_position-=4

			if score==0 and startover==False:
				pipe_group.empty()
				skypipe_group.empty()
				player.sprite.gravity=0
				player.sprite.rect.bottom=256

				get_ready_message=pygame.image.load('graphics/message.png').convert_alpha()
				get_ready_message_rect=get_ready_message.get_rect(center=(get_ready_x_pos,get_ready_y_pos))		
				screen.blit(get_ready_message,get_ready_message_rect)

			elif score ==0 and startover==True:
				screen.blit(game_over_message,game_over_message_rect)

				score_message = flappy_font.render(f'Your Score: {currScore}',False,'#F0AF35')
				score_message_rect = score_message.get_rect(center = (253,150))

				score_message_black1 = flappy_font.render(f'Your Score: {currScore}',False,'#000000')
				score_message_rect_black1 = score_message.get_rect(center = (249,146))
				score_message_black2 = flappy_font.render(f'Your Score: {currScore}',False,'#000000')
				score_message_rect_black2 = score_message.get_rect(center = (257,146))
				score_message_black3 = flappy_font.render(f'Your Score: {currScore}',False,'#000000')
				score_message_rect_black3 = score_message.get_rect(center = (249,154))
				score_message_black4 = flappy_font.render(f'Your Score: {currScore}',False,'#000000')
				score_message_rect_black4 = score_message.get_rect(center = (257,154))

				score_message_white1 = flappy_font.render(f'Your Score: {currScore}',False,'#ffffff')
				score_message_rect_white1 = score_message.get_rect(center = (251,148))
				score_message_white2 = flappy_font.render(f'Your Score: {currScore}',False,'#ffffff')
				score_message_rect_white2= score_message.get_rect(center = (255,148))
				score_message_white3 = flappy_font.render(f'Your Score: {currScore}',False,'#ffffff')
				score_message_rect_white3 = score_message.get_rect(center = (251,152))
				score_message_white4 = flappy_font.render(f'Your Score: {currScore}',False,'#ffffff')
				score_message_rect_white4 = score_message.get_rect(center = (255,152))

				screen.blit(score_message_black1,score_message_rect_black1)
				screen.blit(score_message_black2,score_message_rect_black2)
				screen.blit(score_message_black3,score_message_rect_black3)
				screen.blit(score_message_black4,score_message_rect_black4)

				screen.blit(score_message_white1,score_message_rect_white1)
				screen.blit(score_message_white2,score_message_rect_white2)
				screen.blit(score_message_white3,score_message_rect_white3)
				screen.blit(score_message_white4,score_message_rect_white4)
				screen.blit(score_message,score_message_rect)

				space_message = flappy_font1.render('Press Space Key to continue',False,'#F0AF35')
				space_message_rect = space_message.get_rect(center = (253,250))

				space_message_black1 = flappy_font1.render('Press Space Key to continue',False,'#000000')
				space_message_rect_black1 = space_message.get_rect(center = (249,246))
				space_message_black2 = flappy_font1.render('Press Space Key to continue',False,'#000000')
				space_message_rect_black2 = space_message.get_rect(center = (257,246))
				space_message_black3 = flappy_font1.render('Press Space Key to continue',False,'#000000')
				space_message_rect_black3 = space_message.get_rect(center = (249,254))
				space_message_black4 = flappy_font1.render('Press Space Key to continue',False,'#000000')
				space_message_rect_black4 = space_message.get_rect(center = (257,254))

				space_message_white1 = flappy_font1.render('Press Space Key to continue',False,'#ffffff')
				space_message_rect_white1 = space_message.get_rect(center = (251,248))
				space_message_white2 = flappy_font1.render('Press Space Key to continue',False,'#ffffff')
				space_message_rect_white2= space_message.get_rect(center = (255,248))
				space_message_white3 = flappy_font1.render('Press Space Key to continue',False,'#ffffff')
				space_message_rect_white3 = space_message.get_rect(center = (251,252))
				space_message_white4 = flappy_font1.render('Press Space Key to continue',False,'#ffffff')
				space_message_rect_white4 = space_message.get_rect(center = (255,252))

				
				screen.blit(space_message_black1,space_message_rect_black1)
				screen.blit(space_message_black2,space_message_rect_black2)
				screen.blit(space_message_black3,space_message_rect_black3)
				screen.blit(space_message_black4,space_message_rect_black4)

				screen.blit(space_message_white1,space_message_rect_white1)
				screen.blit(space_message_white2,space_message_rect_white2)
				screen.blit(space_message_white3,space_message_rect_white3)
				screen.blit(space_message_white4,space_message_rect_white4)

				screen.blit(space_message,space_message_rect)

			elif score>0:
				save_score(score)
				score=0
				startover=True

			if base_x_position <-600:
				base_x_position=500
			screen.blit(base_surface_scaled,(base_x_position,450))

			base_x_position_2-=4
			if base_x_position_2 <-600:
				base_x_position_2=500
			screen.blit(base_surface_scaled,(base_x_position_2,450))
			

		
		#else: screen.blit(get_ready_message_rect,())



	pygame.display.update()
	clock.tick(60)

			
