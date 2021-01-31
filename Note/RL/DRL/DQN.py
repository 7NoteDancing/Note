import tensorflow as tf
import numpy as np
import pickle
import time


class DQN:
    def __init__(self,value_net,estimate_p,target_p,state,state_name,action_name,exploration_space,epsilon=None,discount=None,episode_step=None,pool_size=None,batch=None,update_step=None,optimizer=None,lr=None,save_episode=True):
        self.value_net=value_net
        self.estimate_p=estimate_p
        self.target_p=target_p
        self.state_pool=None
        self.action_pool=None
        self.next_state_pool=None
        self.reward_pool=None
        self.episode=[]
        self.state=state
        self.state_name=state_name
        self.action_name=action_name
        self.exploration_space=exploration_space
        self.action_len=len(self.action_name)
        self.epsilon=epsilon
        self.discount=discount
        self.episode_step=episode_step
        self.pool_size=pool_size
        self.batch=batch
        self.update_step=update_step
        self.lr=lr
        self.optimizer=optimizer
        self.save_episode=save_episode
        self.opt_flag==False
        self.a=0
        self._random=None
        self.epi_num=0
        self.episode_num=0
        self.total_episode=0
        self.time=0
        self.total_time=0
    
    
    def init(self,dtype=np.int32):
        self.t3=time.time()
        if len(self.action_name)>self.action_len:
            self.action=np.concatenate((self.action,np.arange(len(self.action_name)-self.action_len,dtype=dtype)+self.action_len))
            self.action_one=np.concatenate((self.action_one,np.ones(len(self.action_name)-self.action_len,dtype=dtype)))
        else:
            self.action=np.arange(len(self.action_name),dtype=dtype)
            self.action_one=np.ones(len(self.action_name),dtype=dtype)
        self.index=np.arange(self.batch,dtype=np.int8)
        if self._random!=None:
            self._random=np.arange(self.pool_size)
        self.t4=time.time()
        return
    
    
    def epsilon_greedy_policy(self,s,action_one):
        action_prob=action_one
        action_prob=action_prob*self.epsilon/len(action_one)
        best_a=np.argmax(self.value_net(self.state[self.state_name[s]]))
        action_prob[best_a]+=1-self.epsilon
        return action_prob
    
    
    def batch(self,index1,index2):
        if len(self.state_pool)<self.pool_size:
            self.random=np.arange(len(self.state_pool))
        else:
            self.random=self._random
        np.random.shuffle(self.random)
        if index1==self.batches*self.batch:
            return self.state_pool[np.concatenate([self.random[index1:],self.random[:index2]])],self.action_pool[np.concatenate([self.random[index1:],self.random[:index2]])],self.next_state_pool[np.concatenate([self.random[index1:],self.random[:index2]])],self.reward_pool[np.concatenate([self.random[index1:],self.random[:index2]])]
        else:
            return self.state_pool[self.random[index1:index2]],self.action_pool[self.random[index1:index2]],self.next_state_pool[self.random[index1:index2]],self.reward_pool[self.random[index1:index2]]
    
    
    def update_parameter(self):
        for i in range(len(self.estimate_p)):
            self.target_p[i]=self.estimate_p[i].copy()
        return
    
    
    def loss(self,s,a,next_s,r):
        if len(self.state_pool)<self.batch:
            return tf.reduce_mean(((r+self.discount*tf.reduce_max(self.value_net(next_s,self.target_p),axis=-1))-self.value_net(s,self.estimate_p)[np.arange(len(a)),a])**2)
        else:
            return tf.reduce_mean(((r+self.discount*tf.reduce_max(self.value_net(next_s,self.target_p),axis=-1))-self.value_net(s,self.estimate_p)[self.index,a])**2)
    
    
    def learn(self,episode_num,path=None,one=True):
        for i in range(episode_num):
            episode=[]
            s=int(np.random.uniform(0,len(self.state_name)))
            if self.episode_step==None:
                while True:
                    t1=time.time()
                    self.a+=1
                    action_prob=self.epsilon_greedy_policy(s,self.action_one)
                    a=np.random.choice(self.action,p=action_prob)
                    next_s,r,end=self.exploration_space[self.state_name[s]][self.action_name[a]]
                    if self.state_pool==None:
                        self.state_pool=tf.expand_dims(self.state[self.state_name[s]],axis=0)
                        self.action_pool=tf.expand_dims(a,axis=0)
                        self.next_state_pool=tf.expand_dims(self.state[self.state_name[next_s]],axis=0)
                        self.reward_pool=tf.expand_dims(r,axis=0)
                    else:
                        self.state_pool=tf.concat([self.state_pool,tf.expand_dims(self.state[self.state_name[s]],axis=0)])
                        self.action_pool=tf.concat([self.action_pool,tf.expand_dims(a,axis=0)])
                        self.next_state_pool=tf.concat([self.next_state_pool,tf.expand_dims(self.state[self.state_name[next_s]],axis=0)])
                        self.reward_pool=tf.concat([self.reward_pool,tf.expand_dims(r,axis=0)])
                    if len(self.state_pool)>self.pool_size:
                        self.state_pool=self.state_pool[1:]
                        self.action_pool=self.action_pool[1:]
                        self.next_state_pool=self.next_state_pool[1:]
                        self.reward_pool=self.reward_pool[1:]
                    if end:
                        if self.save_episode==True:
                            episode.append([self.state_name[s],self.action_name[a],r,end])
                    elif self.save_episode==True:
                        episode.append([self.state_name[s],self.self.action_name[a],r])
                    s=next_s
                    if len(self.state_pool)<self.batch:
                        loss=self.loss(self.state_pool,self.action_pool,self.next_state_pool,self.reward_pool)
                        with tf.GradientTape() as tape:
                            gradient=tape.gradient(loss,self.estimate_p)
                            if self.opt_flag==True:
                                self.optimizer(gradient,self.estimate_p)
                            else:
                                self.optimizer.apply_gradients(zip(gradient,self.estimate_p))
                        if self.a%self.update_step==0:
                            self.update_parameter()
                    else:
                        self.batches=int((len(self.state_pool)-len(self.state_pool)%self.batch)/self.batch)
                        loss=0
                        for j in range(self.batches):
                            index1=j*self.batch
                            index2=(j+1)*self.batch
                            state_batch,action_batch,next_state_batch,reward_batch=self.batch(j,index1,index2)
                            batch_loss=self.loss(state_batch,action_batch,next_state_batch,reward_batch)
                            with tf.GradientTape() as tape:
                                gradient=tape.gradient(batch_loss,self.estimate_p)
                                if self.opt_flag==True:
                                    self.optimizer(gradient,self.estimate_p)
                                else:
                                    self.optimizer.apply_gradients(zip(gradient,self.estimate_p))
                            loss+=batch_loss
                        if len(self.state_pool)%self.batch!=0:
                            self.batches+=1
                            index1=self.batches*self.batch
                            index2=self.batch-(len(self.state_pool)-self.batches*self.batch)
                            state_batch,action_batch,next_state_batch,reward_batch=self.batch(j,index1,index2)
                            batch_loss=self.loss(state_batch,action_batch,next_state_batch,reward_batch)
                            with tf.GradientTape() as tape:
                                gradient=tape.gradient(batch_loss,self.estimate_p)
                                if self.opt_flag==True:
                                    self.optimizer(gradient,self.estimate_p)
                                else:
                                    self.optimizer.apply_gradients(zip(gradient,self.estimate_p))
                            loss+=batch_loss
                        if len(self.state_pool)%self.batch!=0:
                            loss=loss.numpy()/self.batches+1
                        elif len(self.state_pool)<self.batch:
                            loss=loss.numpy()
                        else:
                            loss=loss.numpy()/self.batches
                        if self.a%self.update_step==0:
                            self.update_parameter()
                    t2=time.time()
                    self.time+=(t2-t1)

            else:
                for _ in range(self.episode_step):
                    t1=time.time()
                    self.a+=1
                    action_prob=self.epsilon_greedy_policy(s,self.action_one)
                    a=np.random.choice(self.action,p=action_prob)
                    next_s,r,end=self.exploration_space[self.state_name[s]][self.action_name[a]]
                    if self.state_pool==None:
                        self.state_pool=tf.expand_dims(self.state[self.state_name[s]],axis=0)
                        self.action_pool=tf.expand_dims(a,axis=0)
                        self.next_state_pool=tf.expand_dims(self.state[self.state_name[next_s]],axis=0)
                        self.reward_pool=tf.expand_dims(r,axis=0)
                    else:
                        self.state_pool=tf.concat([self.state_pool,tf.expand_dims(self.state[self.state_name[s]],axis=0)])
                        self.action_pool=tf.concat([self.action_pool,tf.expand_dims(a,axis=0)])
                        self.next_state_pool=tf.concat([self.next_state_pool,tf.expand_dims(self.state[self.state_name[next_s]],axis=0)])
                        self.reward_pool=tf.concat([self.reward_pool,tf.expand_dims(r,axis=0)])
                    if len(self.state_pool)>self.pool_size:
                        self.state_pool=self.state_pool[1:]
                        self.action_pool=self.action_pool[1:]
                        self.next_state_pool=self.next_state_pool[1:]
                        self.reward_pool=self.reward_pool[1:]
                    if end:
                        if self.save_episode==True:
                            episode.append([self.state_name[s],self.action_name[a],r,end])
                        break
                    elif self.save_episode==True:
                        episode.append([self.state_name[s],self.self.action_name[a],r])
                    s=next_s
                    if len(self.state_pool)<self.batch:
                        loss=self.loss(self.state_pool,self.action_pool,self.next_state_pool,self.reward_pool)
                        with tf.GradientTape() as tape:
                            gradient=tape.gradient(loss,self.estimate_p)
                            if self.opt_flag==True:
                                self.optimizer(gradient,self.estimate_p)
                            else:
                                self.optimizer.apply_gradients(zip(gradient,self.estimate_p))
                        if self.a%self.update_step==0:
                            self.update_parameter()
                    else:
                        self.batches=int((len(self.state_pool)-len(self.state_pool)%self.batch)/self.batch)
                        loss=0
                        for j in range(self.batches):
                            index1=j*self.batch
                            index2=(j+1)*self.batch
                            state_batch,action_batch,next_state_batch,reward_batch=self.batch(j,index1,index2)
                            batch_loss=self.loss(state_batch,action_batch,next_state_batch,reward_batch)
                            with tf.GradientTape() as tape:
                                gradient=tape.gradient(batch_loss,self.estimate_p)
                                if self.opt_flag==True:
                                    self.optimizer(gradient,self.estimate_p)
                                else:
                                    self.optimizer.apply_gradients(zip(gradient,self.estimate_p))
                            loss+=batch_loss
                        if len(self.state_pool)%self.batch!=0:
                            self.batches+=1
                            index1=self.batches*self.batch
                            index2=self.batch-(len(self.state_pool)-self.batches*self.batch)
                            state_batch,action_batch,next_state_batch,reward_batch=self.batch(j,index1,index2)
                            batch_loss=self.loss(state_batch,action_batch,next_state_batch,reward_batch)
                            with tf.GradientTape() as tape:
                                gradient=tape.gradient(batch_loss,self.estimate_p)
                                if self.opt_flag==True:
                                    self.optimizer(gradient,self.estimate_p)
                                else:
                                    self.optimizer.apply_gradients(zip(gradient,self.estimate_p))
                            loss+=batch_loss
                        if len(self.state_pool)%self.batch!=0:
                            loss=loss.numpy()/self.batches+1
                        elif len(self.state_pool)<self.batch:
                            loss=loss.numpy()
                        else:
                            loss=loss.numpy()/self.batches
                        if self.a%self.update_step==0:
                            self.update_parameter()
                    t2=time.time()
                    self.time+=(t2-t1)
            if episode_num%10!=0:
                d=episode_num-episode_num%10
                d=int(d/10)
            else:
                d=episode_num/10
            if d==0:
                d=1
            if i%d==0:
                print('episode num:{0}   loss:{1:.6f}'.format(i+1,loss))
                if path!=None and i%episode_num*2==0:
                    self.save(path,i,one)
            self.epi_num+=1
            self.total_episode+=1
            if self.save_episode==True:
                self.episode.append(episode)
        if self.time<0.5:
            self.time=int(self.time+(self.t4-self.t3))
        else:
            self.time=int(self.time+(self.t4-self.t3))+1
        self.total_time+=self.time
        print()
        print('last loss:{0:.6f}'.format(loss))
        print('time:{0}s'.format(self.time))
        return
    
    
    def save(self,path,i=None,one=True):
        if one==True:
            output_file=open(path+'.dat','wb')
        else:
            output_file=open(path+'-{0}.dat'.format(i+1),'wb')
        self.episode_num=self.epi_num
        pickle.dump(self.state_pool,output_file)
        pickle.dump(self.action_pool,output_file)
        pickle.dump(self.next_state_pool,output_file)
        pickle.dump(self.reward_pool,output_file)
        pickle.dump(self.episode,output_file)
        pickle.dump(self.action_len,output_file)
        pickle.dump(self.action,output_file)
        pickle.dump(self.action_one,output_file)
        pickle.dump(self.index,output_file)
        pickle.dump(self.epsilon,output_file)
        pickle.dump(self.discount,output_file)
        pickle.dump(self.episode_step,output_file)
        pickle.dump(self.pool_size,output_file)
        pickle.dump(self.batch,output_file)
        pickle.dump(self.update_step,output_file)
        pickle.dump(self.lr,output_file)
        pickle.dump(self.optimizer,output_file)
        pickle.dump(self.save_episode,output_file)
        pickle.dump(self.opt_flag,output_file)
        pickle.dump(self.a,output_file)
        pickle.dump(self._random,output_file)
        pickle.dump(self.episode_num,output_file)
        pickle.dump(self.total_episode,output_file)
        pickle.dump(self.total_time,output_file)
        output_file.close()
        return
    
    
    def restore(self,path):
        input_file=open(path,'rb')
        self.state_pool=pickle.load(input_file)
        self.action_pool=pickle.load(input_file)
        self.next_state_pool=pickle.load(input_file)
        self.reward_pool=pickle.load(input_file)
        self.episode=pickle.load(input_file)
        self.action_len=pickle.load(input_file)
        self.action=pickle.load(input_file)
        self.action_one=pickle.load(input_file)
        self.index=pickle.load(input_file)
        self.epsilon=pickle.load(input_file)
        self.discount=pickle.load(input_file)
        self.episode_step=pickle.load(input_file)
        self.pool_size=pickle.load(input_file)
        self.batch=pickle.load(input_file)
        self.update_step=pickle.load(input_file)
        self.lr=pickle.load(input_file)
        self.optimizer=pickle.load(input_file)
        self.save_episode=pickle.load(input_file)
        self.opt_flag=pickle.load(input_file)
        self.a=pickle.load(input_file)
        self._random=pickle.load(input_file)
        self.episode_num=pickle.load(input_file)
        self.total_episode=pickle.load(input_file)
        self.total_time=self.time
        input_file.close()
        return
