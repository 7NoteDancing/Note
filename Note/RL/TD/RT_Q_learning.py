import numpy as np
import time


class RT_Q_learning:
    def __init__(self,q,state_name,action_name,exploration_space,epsilon,alpha,discount,dst,episode_step=None,save_episode=True):
        self.q=q
        self.episode=[]
        self.state_name=state_name
        self.action_name=action_name
        self.exploration_space=exploration_space
        self.epsilon=epsilon
        self.alpha=alpha
        self.discount=discount
        self.dst=dst
        self.episode_step=episode_step
        self.save_episode=save_episode
    
    
    def init(self,dtype=np.int32):
        self.t3=time.time()
        if len(self.action_name)>self.q.shape[1]:
            self.action=np.concatenate((self.action,np.arange(len(self.action_name)-self.q.shape[1],dtype=dtype)+self.q.shape[1]))
            self.action_prob=np.concatenate((self.action_prob,np.ones(len(self.action_name)-self.q.shape[1],dtype=dtype)))
        else:
            self.action=np.arange(len(self.action_name),dtype=dtype)
            self.action_prob=np.ones(len(self.action_name),dtype=dtype)
        if len(self.state_name)>self.q.shape[0] or len(self.action_name)>self.q.shape[1]:
            self.q=np.concatenate((self.q,np.zeros([len(self.state_name),len(self.action_name)-self.action_len],dtype=self.q.dtype)),axis=1)
            self.q=np.concatenate((self.q,np.zeros([len(self.state_name)-self.state_len,len(self.action_name)],dtype=self.q.dtype)))
            self.q=self.q.numpy()
        self.t4=time.time()
        return


    def epsilon_greedy_policy(self,q,s,action_one):
        action_prob=action_one
        action_prob=action_prob*self.epsilon/len(action_one)
        best_a=np.argmax(q[s])
        action_prob[best_a]+=1-self.epsilon
        return action_prob
    
    
    def td(self,q,s,a,next_s,reward):
        q[s][a]=q[s][a]+self.alpha*(reward+self.discount*np.max(q[next_s])-q[s][a])
        return q,next_s
    
    
    def RT_update_q(self,q,s,action,action_one):
        a=0
        delta=0
        while True:
            t1=time.time()
            a+=1
            action_prob=self.epsilon_greedy_policy(q,s,action_one)
            a=np.random.choice(np.arange(action_prob.shape[0]),p=action_prob)
            next_s,reward,end=self.exploration_space[self.state_name[s]][self.action_name[a]]
            temp=q[s][a]
            delta+=np.abs(q[s][a]-temp)
            q,next_s=self.td(q,s,a,next_s,reward)
            s=next_s
            self.dst[0]=delta/self.dst[1]
            self.dst[1]+=1
            if self.save_episode==True and a<=self.episode_step:
                self.episode.append([self.state_name[s],self.action_name[a],reward])
            t2=time.time()
            _time=t2-t1+self.t4-self.t3
            self.dst[2]+=_time
        return
    
    
    def learn(self):
        s=int(np.random.uniform(0,len(self.state_name)))
        self.q=self.RT_update_q(self.q,s,self.action,self.action_prob)
        return
