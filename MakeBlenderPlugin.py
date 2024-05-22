import bpy, subprocess, os

bl_info = {
	'name': 'Blender Plugin',
	'blender': (2, 80, 0),
	'category': 'System',
}
REPLACE_INDICATOR = 'ꗈ'
GAME_OBJECT_TEMPLATE = '''--- !u!1 &ꗈ0
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  serializedVersion: 6
  m_Component:
  - component: {fileID: ꗈ1}
ꗈ2
  m_Layer: 0
  m_Name: ꗈ3
  m_TagString: Untagged
  m_Icon: {fileID: 0}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1'''
TRANSFORM_TEMPLATE = '''--- !u!4 &ꗈ0
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: ꗈ1}
  serializedVersion: 2
  m_LocalRotation: {x: ꗈ2, y: ꗈ3, z: ꗈ4, w: ꗈ5}
  m_LocalPosition: {x: ꗈ6, y: ꗈ7, z: ꗈ8}
  m_LocalScale: {x: ꗈ9, y: ꗈ10, z: ꗈ11}
  m_ConstrainProportionsScale: 0
  m_Children: []
  m_Father: {fileID: 0}
  m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}'''
LIGHT_TEMPLATE = '''--- !u!108 &ꗈ0
Light:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: ꗈ1}
  m_Enabled: 1
  serializedVersion: 11
  m_Type: ꗈ2
  m_Color: {r: ꗈ3, g: ꗈ4, b: ꗈ5, a: 1}
  m_Intensity: ꗈ6
  m_Range: ꗈ7
  m_SpotAngle: ꗈ8
  m_InnerSpotAngle: ꗈ9
  m_CookieSize: 10
  m_Shadows:
    m_Type: 0
    m_Resolution: -1
    m_CustomResolution: -1
    m_Strength: 1
    m_Bias: 0.05
    m_NormalBias: 0.4
    m_NearPlane: 0.2
    m_CullingMatrixOverride:
      e00: 1
      e01: 0
      e02: 0
      e03: 0
      e10: 0
      e11: 1
      e12: 0
      e13: 0
      e20: 0
      e21: 0
      e22: 1
      e23: 0
      e30: 0
      e31: 0
      e32: 0
      e33: 1
    m_UseCullingMatrixOverride: 0
  m_Cookie: {fileID: 0}
  m_DrawHalo: 0
  m_Flare: {fileID: 0}
  m_RenderMode: 0
  m_CullingMask:
    serializedVersion: 2
    m_Bits: 4294967295
  m_RenderingLayerMask: 1
  m_Lightmapping: 4
  m_LightShadowCasterMode: 0
  m_AreaSize: {x: 1, y: 1}
  m_BounceIntensity: 1
  m_ColorTemperature: 6570
  m_UseColorTemperature: 0
  m_BoundingSphereOverride: {x: 0, y: 0, z: 0, w: 0}
  m_UseBoundingSphereOverride: 0
  m_UseViewFrustumForShadowCasterCull: 1
  m_ShadowRadius: 0
  m_ShadowAngle: 0'''
SCRIPT_TEMPLATE = '''--- !u!114 &ꗈ0
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: ꗈ1}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {fileID: 11500000, guid: ꗈ2, type: 3}
  m_Name: 
  m_EditorClassIdentifier: 
  m_Version: 3
  m_UsePipelineSettings: 1
  m_AdditionalLightsShadowResolutionTier: 2
  m_LightLayerMask: 1
  m_RenderingLayers: 1
  m_CustomShadowLayers: 0
  m_ShadowLayerMask: 1
  m_ShadowRenderingLayers: 1
  m_LightCookieSize: {x: 1, y: 1}
  m_LightCookieOffset: {x: 0, y: 0}
  m_SoftShadowQuality: 0'''
# SCRIPT_META_TEMPLATE = '''fileFormatVersion: 2
# guid: '''
MESH_FILTER_TEMPLATE = '''--- !u!33 &ꗈ0
MeshFilter:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: ꗈ1}
  m_Mesh: {fileID: ꗈ2, guid: ꗈ3, type: 3}'''
MESH_RENDERER_TEMPLATE = '''--- !u!23 &ꗈ0
MeshRenderer:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: ꗈ1}
  m_Enabled: 1
  m_CastShadows: 1
  m_ReceiveShadows: 1
  m_DynamicOccludee: 1
  m_StaticShadowCaster: 0
  m_MotionVectors: 1
  m_LightProbeUsage: 1
  m_ReflectionProbeUsage: 1
  m_RayTracingMode: 2
  m_RayTraceProcedural: 0
  m_RayTracingAccelStructBuildFlagsOverride: 0
  m_RayTracingAccelStructBuildFlags: 1
  m_RenderingLayerMask: 1
  m_RendererPriority: 0
  m_Materials:
  - {fileID: 10303, guid: 0000000000000000f000000000000000, type: 0}
  m_StaticBatchInfo:
    firstSubMesh: 0
    subMeshCount: 0
  m_StaticBatchRoot: {fileID: 0}
  m_ProbeAnchor: {fileID: 0}
  m_LightProbeVolumeOverride: {fileID: 0}
  m_ScaleInLightmap: 1
  m_ReceiveGI: 1
  m_PreserveUVs: 0
  m_IgnoreNormalsForChartDetection: 0
  m_ImportantGI: 0
  m_StitchLightmapSeams: 1
  m_SelectedEditorRenderState: 3
  m_MinimumChartSize: 4
  m_AutoUVMaxDistance: 0.5
  m_AutoUVMaxAngle: 89
  m_LightmapParameters: {fileID: 0}
  m_SortingLayerID: 0
  m_SortingLayer: 0
  m_SortingOrder: 0
  m_AdditionalVertexStreams: {fileID: 0}'''
COMPONENT_TEMPLATE = '  - component: {fileID: ꗈ}'
SCENE_ROOT_TEMPLATE = '  - {fileID: ꗈ}'
lastId = 5

class TEXT_EDITOR_OT_UnrealExportButton (bpy.types.Operator):
	bl_idname = 'unreal.export'
	bl_label = 'Export To Unreal'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		command = [ 'python3', os.path.expanduser('~/Unity2Many/UnityToUnreal.py'), 'input=' + os.path.expanduser(context.scene.world.unity_project_import_path), 'output=' + os.path.expanduser(context.scene.world.unreal_project_path), 'exclude=/Library' ]

		subprocess.check_call(command)

class TEXT_EDITOR_OT_BevyExportButton (bpy.types.Operator):
	bl_idname = 'bevy.export'
	bl_label = 'Export To Bevy'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		command = [ 'python3', os.path.expanduser('~/Unity2Many/UnityToBevy.py'), 'input=' + os.path.expanduser(context.scene.world.unity_project_import_path), 'output=' + os.path.expanduser(context.scene.world.bevy_project_path), 'exclude=/Library' ]

		subprocess.check_call(command)

class TEXT_EDITOR_OT_UnityExportButton (bpy.types.Operator):
	bl_idname = 'unity.export'
	bl_label = 'Export To Unity'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		global lastId
		projectExportPath = os.path.expanduser(context.scene.world.unity_project_export_path)
		for textBlock in bpy.data.texts:
			text = textBlock.as_string()
			fileExportPath = projectExportPath + '/Assets/Standard Assets/Scripts/' + textBlock.name + '.cs'
			MakeFolderForFile (fileExportPath)
			open(fileExportPath, 'wb').write(text.encode('utf-8'))
		meshesDict = {}
		for mesh in bpy.data.meshes:
			meshesDict[mesh.name] = []
		for obj in bpy.context.scene.objects:
			if obj.type == 'MESH' and obj.data.name in meshesDict:
				meshesDict[obj.data.name].append(obj.name)
				fileExportPath = projectExportPath + '/Assets/Art/Models/' + obj.data.name + '.fbx'
				MakeFolderForFile (fileExportPath)
				bpy.ops.object.select_all(action='DESELECT')
				bpy.context.view_layer.objects.active = obj
				obj.select_set(True)
				bpy.ops.export_scene.fbx(filepath=fileExportPath, use_selection=True)
		MakeFolderForFile (projectExportPath + '/Assets/Editor/GetUnityProjectInfo.cs')

		os.system('cp ' + os.path.expanduser('~/Unity2Many/GetUnityProjectInfo.cs') + ' ' + projectExportPath + '/Assets/Editor/GetUnityProjectInfo.cs')
		os.system('cp ' + os.path.expanduser('~/Unity2Many/SystemExtensions.cs') + ' ' + projectExportPath + '/Assets/Editor/SystemExtensions.cs')

		command = [os.path.expanduser('~/Unity/Hub/Editor/' + context.scene.world.unity_export_version + '/Editor/Unity'), '-createProject', projectExportPath, '-quit', '-executeMethod', 'GetUnityProjectInfo.Do', os.path.expanduser(context.scene.world.unity_project_export_path) ]
		
		subprocess.check_call(command)

		scenePath = bpy.data.filepath.replace('.blend', '.unity')
		scenePath = scenePath[scenePath.rfind('/') + 1 :]
		scenesFolderPath = projectExportPath + '/Assets/Scenes'
		if not os.path.isdir(scenesFolderPath):
			os.mkdir(scenesFolderPath)
		scenePath = scenesFolderPath + '/' + scenePath
		sceneTemplateText = open(os.path.expanduser('~/Unity2Many/Templates/Scene.unity'), 'rb').read().decode('utf-8')
		gameObjectsAndComponentsText = ''
		transformIds = []
		for obj in bpy.data.objects:
			componentIds = []
			gameObject = GAME_OBJECT_TEMPLATE
			gameObject = gameObject.replace(REPLACE_INDICATOR + '0', str(lastId))
			gameObject = gameObject.replace(REPLACE_INDICATOR + '1', str(lastId + 1))
			gameObject = gameObject.replace(REPLACE_INDICATOR + '3', obj.name)
			gameObjectsAndComponentsText += gameObject + '\n'
			gameObjectId = lastId
			lastId += 1
			transform = TRANSFORM_TEMPLATE
			transform = transform.replace(REPLACE_INDICATOR + '0', str(lastId))
			transform = transform.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
			previousObjectRotationMode = obj.rotation_mode
			obj.rotation_mode = 'QUATERNION'
			transform = transform.replace(REPLACE_INDICATOR + '2', str(obj.rotation_quaternion.x))
			transform = transform.replace(REPLACE_INDICATOR + '3', str(obj.rotation_quaternion.y))
			transform = transform.replace(REPLACE_INDICATOR + '4', str(obj.rotation_quaternion.z))
			transform = transform.replace(REPLACE_INDICATOR + '5', str(obj.rotation_quaternion.w))
			obj.rotation_mode = previousObjectRotationMode
			transform = transform.replace(REPLACE_INDICATOR + '6', str(obj.location.x))
			transform = transform.replace(REPLACE_INDICATOR + '7', str(obj.location.y))
			transform = transform.replace(REPLACE_INDICATOR + '8', str(obj.location.z))
			transform = transform.replace(REPLACE_INDICATOR + '9', str(obj.scale.x))
			transform = transform.replace(REPLACE_INDICATOR + '10', str(obj.scale.y))
			transform = transform.replace(REPLACE_INDICATOR + '11', str(obj.scale.z))
			gameObjectsAndComponentsText += transform + '\n'
			transformIds.append(lastId)
			lastId += 1
			if obj.type == 'LIGHT':
				light = LIGHT_TEMPLATE
				light = light.replace(REPLACE_INDICATOR + '0', str(lastId))
				light = light.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
				lightObject = bpy.data.lights[obj.name]
				lightType = 2
				if lightObject.type == 'SUN':
					lightType = 1
				elif lightObject.type == 'SPOT':
					lightType = 0
				elif lightObject.type == 'AREA':
					lightType = 3
				light = light.replace(REPLACE_INDICATOR + '2', str(lightType))
				light = light.replace(REPLACE_INDICATOR + '3', str(lightObject.color[0]))
				light = light.replace(REPLACE_INDICATOR + '4', str(lightObject.color[1]))
				light = light.replace(REPLACE_INDICATOR + '5', str(lightObject.color[2]))
				light = light.replace(REPLACE_INDICATOR + '6', str(lightObject.energy))
				light = light.replace(REPLACE_INDICATOR + '7', str(10))
				light = light.replace(REPLACE_INDICATOR + '8', str(lightObject.spot_size))
				light = light.replace(REPLACE_INDICATOR + '9', str(lightObject.spot_size * (1.0 - lightObject.spot_blend)))
				gameObjectsAndComponentsText += light + '\n'
				componentIds.append(lastId)
				lastId += 1
			elif obj.type == 'MESH':
				meshFilter = MESH_FILTER_TEMPLATE
				meshFilter = meshFilter.replace(REPLACE_INDICATOR + '0', str(lastId))
				meshFilter = meshFilter.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
				dataText = open('/tmp/Unity2Many Data (BlenderToUnity)', 'rb').read().decode('utf-8')
				fileIdIndicator = '-' + projectExportPath + '/Assets/Art/Models/' + obj.data.name + '.fbx'
				indexOfFile = dataText.find(fileIdIndicator)
				indexOfFileId = indexOfFile + len(fileIdIndicator) + 1
				indexOfEndOfFileId = dataText.find(' ', indexOfFileId)
				fileId = dataText[indexOfFileId : indexOfEndOfFileId]
				indexOfNewLine = dataText.find('\n', indexOfEndOfFileId + 1)
				meshGuid = dataText[indexOfEndOfFileId + 1 : indexOfNewLine]
				meshFilter = meshFilter.replace(REPLACE_INDICATOR + '2', fileId)
				meshFilter = meshFilter.replace(REPLACE_INDICATOR + '3', meshGuid)
				gameObjectsAndComponentsText += meshFilter + '\n'
				componentIds.append(lastId)
				lastId += 1
				meshRenderer = MESH_RENDERER_TEMPLATE
				meshRenderer = meshRenderer.replace(REPLACE_INDICATOR + '0', str(lastId))
				meshRenderer = meshRenderer.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
				gameObjectsAndComponentsText += meshRenderer + '\n'
				componentIds.append(lastId)
				lastId += 1
			for textBlock in bpy.data.texts:
				if textBlock.name == obj.name:
					# scriptMeta = SCRIPT_META_TEMPLATE
					# scriptMeta += str(lastId)
					# lastId += 1
					# open(projectExportPath + '/Assets/Standard Assets/Scripts/' + textBlock.name + '.cs.meta', 'wb').write(scriptMeta.encode('utf-8'))
					script = SCRIPT_TEMPLATE
					script = script.replace(REPLACE_INDICATOR + '0', str(lastId))
					script = script.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
					# script = script.replace(REPLACE_INDICATOR + '2', str(lastId - 1))
					scriptMetaText = open(projectExportPath + '/Assets/Standard Assets/Scripts/' + textBlock.name + '.cs.meta', 'rb').read().decode('utf-8')
					guidIndicator = 'guid: '
					scriptGuid = scriptMetaText[scriptMetaText.find(guidIndicator) + len(guidIndicator) :]
					script = script.replace(REPLACE_INDICATOR + '2', scriptGuid)
					gameObjectsAndComponentsText += script + '\n'
					componentIds.append(lastId)
					lastId += 1
					break
			indexOfComponentsList = gameObjectsAndComponentsText.find(REPLACE_INDICATOR + '2')
			for componentId in componentIds:
				component = COMPONENT_TEMPLATE
				component = component.replace(REPLACE_INDICATOR, str(componentId))
				gameObjectsAndComponentsText = gameObjectsAndComponentsText[: indexOfComponentsList] + component + '\n' + gameObjectsAndComponentsText[indexOfComponentsList :]
				gameObjectsAndComponentsText = gameObjectsAndComponentsText.replace(REPLACE_INDICATOR + '2', '')
		sceneText = sceneTemplateText.replace(REPLACE_INDICATOR + '0', gameObjectsAndComponentsText)
		sceneRootsText = ''
		for transformId in transformIds:
			sceneRoot = SCENE_ROOT_TEMPLATE
			sceneRoot = sceneRoot.replace(REPLACE_INDICATOR, str(transformId))
			sceneRootsText += sceneRoot + '\n'
		sceneText = sceneText.replace(REPLACE_INDICATOR + '1', sceneRootsText)
		open(scenePath, 'wb').write(sceneText.encode('utf-8'))
		command = [os.path.expanduser('~/Unity/Hub/Editor/' + context.scene.world.unity_export_version + '/Editor/Unity'), '-createProject', projectExportPath ]
		
		subprocess.check_call(command)

classes = [
	TEXT_EDITOR_OT_UnrealExportButton,
	TEXT_EDITOR_OT_BevyExportButton,
	TEXT_EDITOR_OT_UnityExportButton
]

def MakeFolderForFile (path : str):
	_path = path[: path.find('/')]
	while _path != path:
		if _path != '' and not os.path.isdir(_path):
			os.mkdir(_path)
		indexOfSlash = path.find('/', len(_path) + 1)
		if indexOfSlash == -1:
			break
		_path = path[: indexOfSlash]

def DrawUnityImportField (self, context):
	self.layout.prop(context.world, 'unity_project_import_path')

def DrawUnityExportPathField (self, context):
	self.layout.prop(context.world, 'unity_project_export_path')

def DrawUnityExportVersionField (self, context):
	self.layout.prop(context.world, 'unity_export_version')

def DrawUnrealExportField (self, context):
	self.layout.prop(context.world, 'unreal_project_path')

def DrawBevyExportField (self, context):
	self.layout.prop(context.world, 'bevy_project_path')

def DrawUnrealExportButton (self, context):
	self.layout.operator('unreal.export', icon='CONSOLE')

def DrawBevyExportButton (self, context):
	self.layout.operator('bevy.export', icon='CONSOLE')

def DrawUnityExportButton (self, context):
	self.layout.operator('unity.export', icon='CONSOLE')

def register ():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.World.unity_project_import_path = bpy.props.StringProperty(
		name = 'Unity project import path',
		description = 'My description',
		default = ''
	)
	bpy.types.World.unity_project_export_path = bpy.props.StringProperty(
		name = 'Unity project export path',
		description = 'My description',
		default = '/tmp/TestUnityProject'
	)
	bpy.types.World.unity_export_version = bpy.props.StringProperty(
		name = 'Unity export version',
		description = 'My description',
		default = ''
	)
	bpy.types.World.unreal_project_path = bpy.props.StringProperty(
		name = 'Unreal project path',
		description = 'My description',
		default = ''
	)
	bpy.types.World.bevy_project_path = bpy.props.StringProperty(
		name = 'Bevy project path',
		description = 'My description',
		default = ''
	)
	bpy.types.TEXT_HT_footer.append(DrawUnrealExportButton)
	bpy.types.TEXT_HT_footer.append(DrawBevyExportButton)
	bpy.types.TEXT_HT_footer.append(DrawUnityExportButton)
	bpy.types.WORLD_PT_context_world.append(DrawUnityImportField)
	bpy.types.WORLD_PT_context_world.append(DrawUnityExportPathField)
	bpy.types.WORLD_PT_context_world.append(DrawUnityExportVersionField)
	bpy.types.WORLD_PT_context_world.append(DrawUnrealExportField)
	bpy.types.WORLD_PT_context_world.append(DrawBevyExportField)

def unregister ():
	bpy.types.TEXT_HT_footer.remove(DrawUnrealExportButton)
	bpy.types.TEXT_HT_footer.remove(DrawBevyExportButton)
	bpy.types.TEXT_HT_footer.remove(DrawUnityExportButton)
	bpy.types.WORLD_PT_context_world.remove(DrawUnityImportField)
	bpy.types.WORLD_PT_context_world.remove(DrawUnityExportPathField)
	bpy.types.WORLD_PT_context_world.remove(DrawUnityExportVersionField)
	bpy.types.WORLD_PT_context_world.remove(DrawUnrealExportField)
	bpy.types.WORLD_PT_context_world.remove(DrawBevyExportField)
	for cls in classes:
		bpy.utils.unregister_class(cls)

if __name__ == '__main__':
	register ()