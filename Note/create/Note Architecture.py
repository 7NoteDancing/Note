import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import time


def write_data(data,path):
    output_file=open(path,'wb')
    pickle.dump(data,output_file)
    output_file.close()
    return


def read_data(path,dtype=np.float32):
    input_file=open(path,'rb')
    data=pickle.load(input_file)
    return np.array(data,dtype=dtype)


def write_data_csv(data,path,dtype=None,index=False,header=False):
    if dtype==None:
        data=pd.DataFrame(data)
        data.to_csv(path,index=index,header=header)
    else:
        data=np.array(data,dtype=dtype)
        data=pd.DataFrame(data)
        data.to_csv(path,index=index,header=header)
    return
        

def read_data_csv(path,dtype=None,header=None):
    if dtype==None:
        data=pd.read_csv(path,header=header)
        return np.array(data)
    else:
        data=pd.read_csv(path,header=header)
        return np.array(data,dtype=dtype)


class unnamed:
    def __init__():
        self.graph=tf.Graph()
        
        
        with self.graph.as_default():
                
                
        self.batch=None
        self.epoch=0
        self.lr=None
        
        
        self.optimizer=None
        self.train_loss=None
        self.train_acc=None
        self.train_loss_list=[]
        self.train_acc_list=[]
        self.test_loss=None
        self.test_acc=None
        self.continue_train=False
        self.flag=None
        self.end_flag=False
        self.test_flag=None
        self.total_epoch=0
        self.time=0
        self.total_time=0
        self.processor='/gpu:0'
        
    
    def weight_init(self,shape,mean,stddev,name=None):
        return tf.Variable(tf.random.normal(shape=shape,mean=mean,stddev=stddev,dtype=self.dtype),name=name)
            
    
    def bias_init(self,shape,mean,stddev,name=None):
        return tf.Variable(tf.random.normal(shape=shape,mean=mean,stddev=stddev,dtype=self.dtype),name=name)
    
    
    def structure():
        with self.graph.as_default():
            self.continue_train=False
            self.flag=None
            self.end_flag=False
            self.test_flag=False
            self.train_loss_list.clear()
            self.train_acc_list.clear()
            
            
            self.epoch=0
            self.dtype=dtype
            self.total_epoch=0
            self.time=0
            self.total_time=0
    
    
    
    def forward_propagation():
        with self.graph.as_default():
           
            
            
    def train(self,batch=None,epoch=None,optimizer='Adam',lr=0.001,train_summary_path=None,model_path=None,one=True,continue_train=False,processor=None):
        with self.graph.as_default():
            self.batch=batch
            self.optimizer=optimizer
            self.lr=lr
            if continue_train!=True:
                if self.continue_train==True:
                    continue_train=True
                else:
                    self.train_loss_list.clear()
                    self.train_acc_list.clear()
            if self.continue_train==False and continue_train==True:
                self.train_loss_list.clear()
                self.train_acc_list.clear()
                self.continue_train=True
            if cpu_gpu!=None:
                self.cpu_gpu=cpu_gpu
            
            
            with tf.device(train_cpu_gpu):
                if continue_train==True and self.end_flag==True:
                    self.end_flag=False
                    
                    
                if continue_train==True and self.flag==1:
                    self.flag=0
                    
                    
#     －－－－－－－－－－－－－－－forward propagation－－－－－－－－－－－－－－－
                
                
#     －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
                with tf.name_scope('train_loss'):
                    
                    
                if self.optimizer=='Gradient':
                    opt=tf.train.GradientDescentOptimizer(learning_rate=lr).minimize(train_loss)
                if self.optimizer=='RMSprop':
                    opt=tf.train.RMSPropOptimizer(learning_rate=lr).minimize(train_loss)
                if self.optimizer=='Momentum':
                    opt=tf.train.MomentumOptimizer(learning_rate=lr,momentum=0.99).minimize(train_loss)
                if self.optimizer=='Adam':
                    opt=tf.train.AdamOptimizer(learning_rate=lr).minimize(train_loss)
                with tf.name_scope('train_accuracy'):
                        
                        
                if train_summary_path!=None:
                    train_loss_scalar=tf.summary.scalar('train_loss',train_loss)
                    train_merging=tf.summary.merge([train_loss_scalar])
                    train_acc_scalar=tf.summary.scalar('train_accuracy',train_acc)
                    train_merging=tf.summary.merge([train_acc_scalar])
                    train_writer=tf.summary.FileWriter(train_summary_path)
                config=tf.ConfigProto()
                config.gpu_options.allow_growth=True
                config.allow_soft_placement=True
                sess=tf.Session(config=config)
                sess.run(tf.global_variables_initializer())
                self.sess=sess
                if self.total_epoch==0:
                    epoch=epoch+1
                t1=time.time()
                for i in range(epoch):
                    if batch!=None:
                        batches=int((self.shape0-self.shape0%batch)/batch)
                        total_loss=0
                        total_acc=0
                        random=np.arange(self.shape0)
                        np.random.shuffle(random)
                        
                        
                        for j in range(batches):
                            index1=j*batch
                            index2=(j+1)*batch
                            
                            
                            if i==0 and self.total_epoch==0:
                                batch_loss=sess.run(train_loss,feed_dict=feed_dict)
                            else:
                                batch_loss,_=sess.run([train_loss,opt],feed_dict=feed_dict)
                            total_loss+=batch_loss
                            batch_acc=sess.run(train_acc,feed_dict=feed_dict)
                            total_acc+=batch_acc
                        if self.shape0%batch!=0:
                            batches+=1
                            index1=batches*batch
                            index2=batch-(self.shape0-batches*batch)
                            
                            
                            if i==0 and self.total_epoch==0:
                                batch_loss=sess.run(train_loss,feed_dict=feed_dict)
                            else:
                                batch_loss,_=sess.run([train_loss,opt],feed_dict=feed_dict)
                            total_loss+=batch_loss
                            batch_acc=sess.run(train_acc,feed_dict=feed_dict)
                            total_acc+=batch_acc
                        loss=total_loss/batches
                        train_acc=total_acc/batches
                        self.train_loss_list.append(loss.astype(np.float32))
                        self.train_loss=loss
                        self.train_loss=self.train_loss.astype(np.float32)
                        self.train_acc_list.append(train_acc.astype(np.float32))
                        self.train_acc=train_acc
                        self.train_acc=self.train_acc.astype(np.float32)
                    else:
                        random=np.arange(self.shape0)
                        np.random.shuffle(random)


                        if i==0 and self.total_epoch==0:
                            loss=sess.run(train_loss,feed_dict=feed_dict)
                        else:
                            loss,_=sess.run([train_loss,opt],feed_dict=feed_dict)
                        self.train_loss_list.append(loss.astype(np.float32))
                        self.train_loss=loss
                        self.train_loss=self.train_loss.astype(np.float32)
                        acc=sess.run(train_acc,feed_dict=feed_dict)
                        self.train_acc_list.append(acc.astype(np.float32))
                        self.train_acc=acc
                        self.train_acc=self.train_acc.astype(np.float32)
                    if epoch%10!=0:
                        temp_epoch=epoch-epoch%10
                        temp_epoch=int(temp_epoch/10)
                    else:
                        temp_epoch=epoch/10
                    if temp_epoch==0:
                        temp_epoch=1
                    if i%temp_epoch==0:
                        if continue_train==True:
                            print('epoch:{0}   loss:{1:.6f}'.format(self.total_epoch+i+1,self.train_loss))
                        else:
                            print('epoch:{0}   loss:{1:.6f}'.format(i,self.train_loss))
                        if model_path!=None and i%epoch*2==0:
                            self.save(model_path,i,one)
                        if train_summary_path!=None:
                            train_summary=sess.run(train_merging,feed_dict=feed_dict)
                            train_writer.add_summary(train_summary,i)
                t2=time.time()
                _time=int(t2-t1)
                if continue_train!=True or self.time==0:
                    self.total_time=_time
                else:
                    self.total_time+=_time
                self.time=_time
                print()
                print('last loss:{0:.6f}'.format(self.train_loss))
                if len(self.labels_shape)==2:
                    print('acc:{0:.3f}%'.format(self.train_acc*100))
                else:
                    print('acc:{0:.3f}'.format(self.train_acc))
                if train_summary_path!=None:
                    train_writer.close()
                if continue_train==True:
                    
                    
                    sess.run(tf.global_variables_initializer())
                if continue_train==True:
                    if self.total_epoch==0:
                        self.total_epoch=epoch-1
                        self.epoch=epoch-1
                    else:
                        self.total_epoch=self.total_epoch+epoch
                        self.epoch=epoch
                if continue_train!=True:
                    self.epoch=epoch-1
                print('time:{0}s'.format(self.time))
                return
    
    
    def end(self):
        with self.graph.as_default():
            self.end_flag=True
            self.continue_train=False
            
            
            self.sess.close()
            return
    
    
    def test(self,test_data,test_labels,batch=None):
        with self.graph.as_default():
            if or self.test_flag==False:
                use_nn=False
            elif and self.test_flag!=False:
                use_nn=True
            self.test_flag=True
                
                
            config=tf.ConfigProto()
            config.gpu_options.allow_growth=True
            config.allow_soft_placement=True
            sess=tf.Session(config=config)
            sess.run(tf.global_variables_initializer())
            if batch!=None:
                total_test_loss=0
                total_test_acc=0
                test_batches=int((test_data.shape[0]-test_data.shape[0]%batch)/batch)
                for j in range(test_batches):
                    test_data_batch=test_data[j*batch:(j+1)*batch]
                    test_labels_batch=test_labels[j*batch:(j+1)*batch]
                    batch_test_loss=sess.run(test_loss,feed_dict={test_data_placeholder:test_data_batch,test_labels_placeholder:test_labels_batch})
                    total_test_loss+=batch_test_loss
                    batch_test_acc=sess.run(test_acc,feed_dict={test_data_placeholder:test_data_batch,test_labels_placeholder:test_labels_batch})
                    total_test_acc+=batch_test_acc
                if test_data.shape[0]%batch!=0:
                    test_batches+=1
                    test_data_batch=np.concatenate([test_data[batches*batch:],test_data[:batch-(test_data.shape[0]-batches*batch)]])
                    test_labels_batch=np.concatenate([test_labels[batches*batch:],test_labels[:batch-(test_labels.shape[0]-batches*batch)]])
                    batch_test_loss=sess.run(test_loss,feed_dict={test_data_placeholder:test_data_batch,test_labels_placeholder:test_labels_batch})
                    total_test_loss+=batch_test_loss
                    batch_test_acc=sess.run(test_acc,feed_dict={test_data_placeholder:test_data_batch,test_labels_placeholder:test_labels_batch})
                    total_test_acc+=batch_test_acc
                test_loss=total_test_loss/test_batches
                test_acc=total_test_acc/test_batches
                self.test_loss=test_loss
                self.test_acc=test_acc
                self.test_loss=self.test_loss.astype(np.float32)
                self.test_acc=self.test_acc.astype(np.float32)
            else:
                self.test_loss=sess.run(test_loss,feed_dict={test_data_placeholder:test_data,test_labels_placeholder:test_labels})
                self.test_acc=sess.run(test_acc,feed_dict={test_data_placeholder:test_data,test_labels_placeholder:test_labels})
                self.test_loss=self.test_loss.astype(np.float32)
                self.test_acc=self.test_acc.astype(np.float32)
            print('test loss:{0:.6f}'.format(self.test_loss))
            
            
            sess.close()
            return
        
    
    def train_info(self):
        print()
        print('batch:{0}'.format(self.batch))
        print()
        print('epoch:{0}'.format(self.epoch))
        print()
        print('optimizer:{0}'.format(self.optimizer))
        print()
        print('learning rate:{0}'.format(self.lr))
        print()
        print('time:{0:.3f}s'.format(self.time))
        print()
        print('-------------------------------------')
        print()
        print('train loss:{0}'.format(self.train_loss))
        
        
        return
        
    
    def test_info(self):
        print()
        print('test loss:{0}'.format(self.test_loss))
       
        
        return
		
    
    def info(self):
        self.train_info()
        if self.test_flag==True:
            print()
            print('-------------------------------------')
            self.test_info()
        return


    def train_visual(self):
        print()
        plt.figure(1)
        plt.plot(np.arange(self.epoch+1),self.train_loss_list)
        plt.title('train loss')
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.figure(2)
        plt.plot(np.arange(self.epoch+1),self.train_acc_list)
        plt.title('train acc')
        plt.xlabel('epoch')
        plt.ylabel('acc')
        print('train loss:{0}'.format(self.train_loss))
  
    
        return
    
        
    def comparison(self):
        print()
        print('train loss:{0}'.format(self.train_loss))
        print()
        print('train acc:{0:.3f}%'.format(self.train_acc*100))
        print()
        print('-------------------------------------')
        print()
        print('test loss:{0}'.format(self.test_loss))
        
        
        return
    
    
    def save(self,model_path,i=None,one=True):
        if one==True:
            output_file=open(model_path+'.dat','wb')
        else:
            output_file=open(model_path+'-{0}.dat'.format(i+1),'wb')
            
            
        pickle.dump(self.batch,output_file)
        pickle.dump(self.epoch,output_file)
        pickle.dump(self.lr,output_file)
        
        
        pickle.dump(self.optimizer,output_file)
        pickle.dump(self.train_loss,output_file)
        pickle.dump(self.train_acc,output_file)
        pickle.dump(self.test_flag,output_file)
        if self.test_flag==True:
            pickle.dump(self.test_loss,output_file)
            pickle.dump(self.test_acc,output_file)
        pickle.dump(self.train_loss_list,output_file)
        pickle.dump(self.train_accuracy_list,output_file)
        pickle.dump(self.total_epoch,output_file)
        pickle.dump(self.time,output_file)
        pickle.dump(self.total_time,output_file)
        pickle.dump(self.processor,output_file)
        output_file.close()
        return
    

    def restore(self,model_path):
        input_file=open(model_path,'rb')
        
        
        self.graph=tf.Graph()
        with self.graph.as_default():
            
            
        self.batch=pickle.load(input_file)
        self.epoch=pickle.load(input_file)
        self.lr=pickle.load(input_file)
        
        
        self.optimizer=pickle.load(input_file)
        self.train_loss=pickle.load(input_file)
        self.train_acc=pickle.load(input_file)
        self.test_flag=pickle.load(input_file)
        if self.test_flag==True:
            self.test_loss=pickle.load(input_file)
            self.test_accuracy=pickle.load(input_file)
        self.train_loss_list=pickle.load(input_file)
        self.train_acc_list=pickle.load(input_file)
        self.total_epoch=pickle.load(input_file)
        self.time=pickle.load(input_file)
        self.total_time=pickle.load(input_file)
        self.processor=pickle.load(input_file)
        self.flag=1
        input_file.close()
        return
