/*
Auto-generated by: https://github.com/pmndrs/gltfjsx
Command: npx gltfjsx@6.5.0 public/models/Professionalmiami.glb 
*/

import React from 'react'
import { useGraph } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { SkeletonUtils } from 'three-stdlib'

export function Model(props) {
  const { scene } = useGLTF('/Professionalmiami.glb')
  const clone = React.useMemo(() => SkeletonUtils.clone(scene), [scene])
  const { nodes, materials } = useGraph(clone)
  return (
    <group {...props} dispose={null}>
      <group rotation={[-Math.PI / 2, 0, -Math.PI / 2]} scale={0.025}>
        <primitive object={nodes.pelvis} />
        <skinnedMesh name="charactersmodelstm_professionaltm_professional_varfvmdl_cd_1" geometry={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_1.geometry} material={materials.glove_fullfinger} skeleton={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_1.skeleton} morphTargetDictionary={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_1.morphTargetDictionary} morphTargetInfluences={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_1.morphTargetInfluences} />
        <skinnedMesh name="charactersmodelstm_professionaltm_professional_varfvmdl_cd_2" geometry={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_2.geometry} material={materials.tm_professional_lowerbody_varf} skeleton={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_2.skeleton} morphTargetDictionary={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_2.morphTargetDictionary} morphTargetInfluences={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_2.morphTargetInfluences} />
        <skinnedMesh name="charactersmodelstm_professionaltm_professional_varfvmdl_cd_3" geometry={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_3.geometry} material={materials.tm_professional_mask_varf} skeleton={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_3.skeleton} morphTargetDictionary={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_3.morphTargetDictionary} morphTargetInfluences={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_3.morphTargetInfluences} />
        <skinnedMesh name="charactersmodelstm_professionaltm_professional_varfvmdl_cd_4" geometry={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_4.geometry} material={materials.tm_professional_head_varf} skeleton={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_4.skeleton} morphTargetDictionary={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_4.morphTargetDictionary} morphTargetInfluences={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_4.morphTargetInfluences} />
        <skinnedMesh name="charactersmodelstm_professionaltm_professional_varfvmdl_cd_5" geometry={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_5.geometry} material={materials.tm_professional_body_varf} skeleton={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_5.skeleton} morphTargetDictionary={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_5.morphTargetDictionary} morphTargetInfluences={nodes.charactersmodelstm_professionaltm_professional_varfvmdl_cd_5.morphTargetInfluences} />
      </group>
    </group>
  )
}

useGLTF.preload('/Professionalmiami.glb')
