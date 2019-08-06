"""
This file is use to create custom permissions
we need to make sure the person who created an object can update or delete it
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		#read permissions are allowed to any request
		#so we'll always allow GET, HEAD, or OPTIONS requests
		# user = User.objects.get(pk=view.kwargs['id'])
		# if request.user==user:
		# 	return True
		if request.method in permissions.SAFE_METHODS:
			return True
		#write permissions are only allow to the owner of the account
		return obj.owner == request.user

	

	'''
http PUT http://127.0.0.1:8000/api/v1/shops/1/ 
data=(name=uyhfyu hygrwyehd,description=hvfe gvwwdyfg hygfyweuh yhgwuh","location":"jnikloi9pokplo0kio","contact": "+256788565454","email":"jijg@jgf.com"}
	'''