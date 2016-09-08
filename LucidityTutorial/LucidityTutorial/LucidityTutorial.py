import lucidity
project_base    = 'C:/Users/mike.bourbeau/Desktop/_FtrackTest/{project.name}/{sequence.name}/{shot.name}/Production'
production_base = '{0}/Production'.format(project_base)
asset_base      = '{0}/Publish'.format(project_base)
render_base     = '{0}/Render'.format(project_base)
separator = '/'

shot_template  = lucidity.Template('project-base-maya', separator.join([production_base, 'Maya']))
asset_template  = lucidity.Template('asset-base-maya', separator.join([asset_base, 'Maya']))
asset_template  = lucidity.Template('trender-base', separator.join([render_base, 'Maya']))


#data = {
#	'project': {
#		'name': 'project_01'
#	},
#	'sequence': {
#		'name': ['sequence_01', 'sequence_02']
#	},
#	'shot': {
#		'name': 'shot_01'
#	},
#	'task': {
#		'name': 'task_01'
#	}
#}
data = {
	'project': {
		'name': u'projectname_aaaaaaaaaaaaa'
	}, 
	u'task': {
		'name': u'Design'
	}, 
	u'shot': {
		'name': u'Shot_02'
	},
	u'sequence': {
		'name': u'Sequence_02'
	}
}




path = shot_template.format(data)
print path

