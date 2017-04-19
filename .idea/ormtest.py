import pymysql
class Field:
	def __init__(self,column=None,primary_key=False,unique=False,index=False,nullable=True,default=None):
		self.name = None
		self.column = column
		self.primary_key = primary_key
		self.unique = unique
		self.index = index
		self.nullable = nullable
		self.default = default
	def validate(self,value):
		raise NotImplemented

	def __get__(self, instance, owner):
		if instance is None:
			return self
		return instance.__dict__.get(self.name)
	def __set__(self, instance, value):
		self.validate(value)
		instance.__dict__[self.name] = value

class IntField(Field):
	def __init__(self,column=None,primary_key=False,unique=False,index=False,nullable=True,default=None,auto_increasement=False):
		super().__init__(column=None,primary_key=False,unique=False,index=False,nullable=True,default=None)
		self.auto_increasement = auto_increasement
	def validate(self,value):
		if value is None:
			return
		if not isinstance(value,int):
			raise TypeError('{}<{}>must be int but {}'.format(self.name,self.column,type(value)))

class StringField(Field):
	def __init__(self,column=None,primary_key=False,unique=False,index=False,nullable=True,default=None,length=45):
		super().__init__(column=None,primary_key=False,unique=False,index=False,nullable=True,default=None)
		self.length = length
	def validate(self,value):
		if value is None:
			return
		if not isinstance(value,str):
			raise TypeError('{}<{}> must be str but {}'.format(self.name,self.column,type(value)))
		if len(value) >= self.length:
			raise ValueError('{}<{}> to long'.format(self.name,self.column))


# class User:
# 	id = IntField(name='id',column='id',primary_key=True,auto_increasement=True)
# 	name = StringField(name='name',column='name',nullable=False,unique=True,length=64)
# 	age = IntField(name='age',column='age')
#
# 	def __init__(self,id,name,age):
# 		self.id = id
# 		self.name = name
# 		self.age = age
#
# 	def save(self,session):
# 		query = '''INSERT INTO `user`(`id`,`name`,`age`) VALUE(%s,%s,%s)'''
# 		session.execute(query,self.id,self.name,self.age)

# class Session:
# 	def __init__(self,conn):
# 		self.conn = conn
# 		self.cur = None
# 	def __enter__(self):
# 		self.cur = self.conn.cursor()
# 		return self
#
# 	def __exit__(self, *args):
# 		self.conn.commit()
# 		self.cur.close()
#
# 	def execute(self,query,*args):
# 		self.cur.execute(query,args)

# class Model:
# 	def save(self):
# 		fields = {}
# 		for name, filed in self.__class__.__dict__.items():
# 			if isinstance(filed,Field):
# 				fields[name] = filed
# 		keys = []
# 		values = []
# 		for name, value in self.__dict__.items():
# 			if name in fields.keys():
# 				keys.append('`{}`'.format(name))
# 				values.append(value)
#
# 		query = '''INSERT INTO `{}` ({}) VALUE ({})'''.format(self.__class__.__table__,','.join(keys),','.join(['%s'] *len(keys)))
# 		print(query)
# 		# cur.execute(query,values)

class ModelMeta(type):
	def __new__(cls, name,bases,attrs):
		if '__table__' not in attrs.keys():
			attrs['__table__'] = name
		mapping = {}
		primary_key = []
		for k,v in attrs.items():
			if isinstance(v,Field):
				v.name = k
				if v.column is None:
					v.column = k
				mapping[k] = v
				if v.primary_key:
					primary_key.append(v)
		attrs['__mapping__'] = mapping
		attrs['__primary_key__'] = primary_key
		return super().__new__(cls,name,bases,attrs)
class Model(metaclass=ModelMeta):
	pass

class User(Model):
	__table__ = 'user'

	id = IntField( primary_key=True, auto_increasement=True)
	name = StringField(nullable=False, unique=True, length=64)
	age = IntField()

class Engine:
	def __init__(self,*args,**kwargs):
		self.conn = pymysql.connect(*args,**kwargs)

	def _get_mapping(self,instance):
		mapping = {}
		for k, v in instance.__dict__.items():
			if k in instance.__class__.__mapping__.keys():
				mapping[instance.__class__.__mapping__[k].column] = v
		return mapping

	def save(self,instance:Model):
		mapping = self._get_mapping(instance)
		query = 'INSERT INTO `{}`({}) VALUE ({})'.format(instance.__class__.__table__,','.join(mapping.keys()),','.join(['%s'] *len(mapping.keys())))
		with self.conn as cur:
			with cur:
				cur.execute(query,fields.values())
	def get(self,cls,key):
		if len(cls.__primary_key__) != 1:
			raise Exception('primary key error')
		query = '''SELECT * FROM `{}` WHERE `{}`={}'''.format(cls.__table__,cls.__primary_key__[0].column)
		with self.conn as cur:
			with cur:
				cur.execute(query,(key,))
				rs = cur.fetchone()
				instance = cls()
				for k,v in cls.__mapping__.items():
					if v.column in res.keys():
						setattr(instance,k,rs[v.column])
				return instance

	def update(self,instance):
		mapping = self._get_mapping(instance)
		columns = ['`{}=%s`'.format(k) for k in mapping.keys()]
		where = ['`{}`=%s'.format(it.column) for it in instance.__class__.__primary_key__]
		query = '''UPDATE `{}` SET {} WHERE {}'''.format(instance.__class__.__table__,','.join(columns),','.join(where))
		params = columns.values() + [getattr(instance,it.name) for it in instance.__class__.__primary_key__]
		with self.conn as cur:
			with cur:
				cur.execute(query,params)