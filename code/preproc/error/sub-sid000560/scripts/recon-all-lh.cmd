

#---------------------------------
# New invocation of recon-all Fri Jun 18 14:22:18 EDT 2021 
#--------------------------------------------
#@# Tessellate lh Fri Jun 18 14:22:21 EDT 2021

 mri_pretess ../mri/filled.mgz 255 ../mri/norm.mgz ../mri/filled-pretess255.mgz 


 mri_tessellate ../mri/filled-pretess255.mgz 255 ../surf/lh.orig.nofix 


 rm -f ../mri/filled-pretess255.mgz 


 mris_extract_main_component ../surf/lh.orig.nofix ../surf/lh.orig.nofix 

#--------------------------------------------
#@# Smooth1 lh Fri Jun 18 14:22:26 EDT 2021

 mris_smooth -nw -seed 1234 ../surf/lh.orig.nofix ../surf/lh.smoothwm.nofix 

#--------------------------------------------
#@# Inflation1 lh Fri Jun 18 14:22:32 EDT 2021

 mris_inflate -no-save-sulc -n 50 ../surf/lh.smoothwm.nofix ../surf/lh.inflated.nofix 

#--------------------------------------------
#@# QSphere lh Fri Jun 18 14:24:04 EDT 2021

 mris_sphere -q -seed 1234 ../surf/lh.inflated.nofix ../surf/lh.qsphere.nofix 

#--------------------------------------------
#@# Fix Topology Copy lh Fri Jun 18 14:26:16 EDT 2021

 cp ../surf/lh.orig.nofix ../surf/lh.orig 


 cp ../surf/lh.inflated.nofix ../surf/lh.inflated 

#@# Fix Topology lh Fri Jun 18 14:26:16 EDT 2021

 mris_fix_topology -rusage /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/touch/rusage.mris_fix_topology.lh.dat -mgz -sphere qsphere.nofix -ga -seed 1234 sub-sid000560 lh 



#---------------------------------
# New invocation of recon-all Mon Jun 21 13:49:23 EDT 2021 
#--------------------------------------------
#@# Make White Surf lh Mon Jun 21 13:49:33 EDT 2021

 mris_make_surfaces -aseg ../mri/aseg.presurf -white white.preaparc -noaparc -whiteonly -mgz -T1 brain.finalsurfs sub-sid000560 lh 

#--------------------------------------------
#@# Smooth2 lh Mon Jun 21 13:55:04 EDT 2021

 mris_smooth -n 3 -nw -seed 1234 ../surf/lh.white.preaparc ../surf/lh.smoothwm 

#--------------------------------------------
#@# Inflation2 lh Mon Jun 21 13:55:11 EDT 2021

 mris_inflate -rusage /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/touch/rusage.mris_inflate.lh.dat -n 50 ../surf/lh.smoothwm ../surf/lh.inflated 

#--------------------------------------------
#@# Curv .H and .K lh Mon Jun 21 13:57:00 EDT 2021

 mris_curvature -w lh.white.preaparc 


 mris_curvature -thresh .999 -n -a 5 -w -distances 10 10 lh.inflated 


#-----------------------------------------
#@# Curvature Stats lh Mon Jun 21 13:58:30 EDT 2021

 mris_curvature_stats -m --writeCurvatureFiles -G -o ../stats/lh.curv.stats -F smoothwm sub-sid000560 lh curv sulc 

#--------------------------------------------
#@# Sphere lh Mon Jun 21 13:58:38 EDT 2021

 mris_sphere -rusage /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/touch/rusage.mris_sphere.lh.dat -seed 1234 ../surf/lh.inflated ../surf/lh.sphere 

#--------------------------------------------
#@# Surf Reg lh Mon Jun 21 14:32:49 EDT 2021

 mris_register -curv -rusage /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/touch/rusage.mris_register.lh.dat ../surf/lh.sphere /opt/freesurfer/average/lh.folding.atlas.acfb40.noaparc.i12.2016-08-02.tif ../surf/lh.sphere.reg 

#--------------------------------------------
#@# Jacobian white lh Mon Jun 21 15:14:12 EDT 2021

 mris_jacobian ../surf/lh.white.preaparc ../surf/lh.sphere.reg ../surf/lh.jacobian_white 

#--------------------------------------------
#@# AvgCurv lh Mon Jun 21 15:14:16 EDT 2021

 mrisp_paint -a 5 /opt/freesurfer/average/lh.folding.atlas.acfb40.noaparc.i12.2016-08-02.tif#6 ../surf/lh.sphere.reg ../surf/lh.avg_curv 

#-----------------------------------------
#@# Cortical Parc lh Mon Jun 21 15:14:20 EDT 2021

 mris_ca_label -l ../label/lh.cortex.label -aseg ../mri/aseg.presurf.mgz -seed 1234 sub-sid000560 lh ../surf/lh.sphere.reg /opt/freesurfer/average/lh.DKaparc.atlas.acfb40.noaparc.i12.2016-08-02.gcs ../label/lh.aparc.annot 

#--------------------------------------------
#@# Make Pial Surf lh Mon Jun 21 15:14:40 EDT 2021

 mris_make_surfaces -orig_white white.preaparc -orig_pial white.preaparc -aseg ../mri/aseg.presurf -mgz -T1 brain.finalsurfs sub-sid000560 lh 

