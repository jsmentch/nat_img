

#---------------------------------
# New invocation of recon-all Fri Jun 18 11:43:33 EDT 2021 

 mri_convert /om4/group/gablab/data/jsmentch/ds003017/sub-sid000560/anat/sub-sid000560_acq-MPRAGE_T1w.nii.gz /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/orig/001.mgz 

#--------------------------------------------
#@# MotionCor Fri Jun 18 11:43:40 EDT 2021

 cp /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/orig/001.mgz /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/rawavg.mgz 


 mri_convert /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/rawavg.mgz /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/orig.mgz --conform_min 


 mri_add_xform_to_header -c /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/transforms/talairach.xfm /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/orig.mgz /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/orig.mgz 

#--------------------------------------------
#@# Talairach Fri Jun 18 11:43:48 EDT 2021

 mri_nu_correct.mni --no-rescale --i orig.mgz --o orig_nu.mgz --n 1 --proto-iters 1000 --distance 50 


 talairach_avi --i orig_nu.mgz --xfm transforms/talairach.auto.xfm 

talairach_avi log file is transforms/talairach_avi.log...

 cp transforms/talairach.auto.xfm transforms/talairach.xfm 

#--------------------------------------------
#@# Talairach Failure Detection Fri Jun 18 11:45:17 EDT 2021

 talairach_afd -T 0.005 -xfm transforms/talairach.xfm 


 awk -f /opt/freesurfer/bin/extract_talairach_avi_QA.awk /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/transforms/talairach_avi.log 


 tal_QC_AZS /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/transforms/talairach_avi.log 

#--------------------------------------------
#@# Nu Intensity Correction Fri Jun 18 11:45:17 EDT 2021

 mri_nu_correct.mni --i orig.mgz --o nu.mgz --uchar transforms/talairach.xfm --cm --n 2 


 mri_add_xform_to_header -c /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/transforms/talairach.xfm nu.mgz nu.mgz 

#--------------------------------------------
#@# Intensity Normalization Fri Jun 18 11:47:01 EDT 2021

 mri_normalize -g 1 -mprage -noconform nu.mgz T1.mgz 



#---------------------------------
# New invocation of recon-all Fri Jun 18 11:50:05 EDT 2021 
#-------------------------------------
#@# EM Registration Fri Jun 18 11:50:06 EDT 2021

 mri_em_register -rusage /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/touch/rusage.mri_em_register.dat -uns 3 -mask brainmask.mgz nu.mgz /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca transforms/talairach.lta 

#--------------------------------------
#@# CA Normalize Fri Jun 18 11:53:07 EDT 2021

 mri_ca_normalize -c ctrl_pts.mgz -mask brainmask.mgz nu.mgz /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca transforms/talairach.lta norm.mgz 

#--------------------------------------
#@# CA Reg Fri Jun 18 11:54:32 EDT 2021

 mri_ca_register -rusage /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/touch/rusage.mri_ca_register.dat -nobigventricles -T transforms/talairach.lta -align-after -mask brainmask.mgz norm.mgz /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca transforms/talairach.m3z 

#--------------------------------------
#@# SubCort Seg Fri Jun 18 13:25:05 EDT 2021

 mri_ca_label -relabel_unlikely 9 .3 -prior 0.5 -align norm.mgz transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca aseg.auto_noCCseg.mgz 


 mri_cc -aseg aseg.auto_noCCseg.mgz -o aseg.auto.mgz -lta /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/transforms/cc_up.lta sub-sid000560 

#--------------------------------------
#@# Merge ASeg Fri Jun 18 14:16:53 EDT 2021

 cp aseg.auto.mgz aseg.presurf.mgz 

#--------------------------------------------
#@# Intensity Normalization2 Fri Jun 18 14:16:53 EDT 2021

 mri_normalize -mprage -aseg aseg.presurf.mgz -mask brainmask.mgz norm.mgz brain.mgz 

#--------------------------------------------
#@# Mask BFS Fri Jun 18 14:19:32 EDT 2021

 mri_mask -T 5 brain.mgz brainmask.mgz brain.finalsurfs.mgz 

#--------------------------------------------
#@# WM Segmentation Fri Jun 18 14:19:36 EDT 2021

 mri_segment -mprage brain.mgz wm.seg.mgz 


 mri_edit_wm_with_aseg -keep-in wm.seg.mgz brain.mgz aseg.presurf.mgz wm.asegedit.mgz 


 mri_pretess wm.asegedit.mgz wm norm.mgz wm.mgz 

#--------------------------------------------
#@# Fill Fri Jun 18 14:21:37 EDT 2021

 mri_fill -a ../scripts/ponscc.cut.log -xform transforms/talairach.lta -segmentation aseg.auto_noCCseg.mgz wm.mgz filled.mgz 



#---------------------------------
# New invocation of recon-all Mon Jun 21 12:50:07 EDT 2021 
#--------------------------------------
#@# SubCort Seg Mon Jun 21 12:50:11 EDT 2021

 mri_seg_diff --seg1 aseg.auto.mgz --seg2 aseg.presurf.mgz --diff aseg.manedit.mgz 


 mri_ca_label -relabel_unlikely 9 .3 -prior 0.5 -align norm.mgz transforms/talairach.m3z /opt/freesurfer/average/RB_all_2016-05-10.vc700.gca aseg.auto_noCCseg.mgz 


 mri_cc -aseg aseg.auto_noCCseg.mgz -o aseg.auto.mgz -lta /om4/group/gablab/data/jsmentch/ds003017/derivatives/freesurfer/sub-sid000560/mri/transforms/cc_up.lta sub-sid000560 

#--------------------------------------
#@# Merge ASeg Mon Jun 21 13:49:08 EDT 2021

 cp aseg.auto.mgz aseg.presurf.mgz 

