C     -*- fortran -*-
C     This file is autogenerated with f2py (version:2)
C     It contains Fortran 77 wrappers to fortran functions.

      subroutine f2pywrapisib_pid2pdg (isib_pid2pdgf2pywrap, npid)
      external isib_pid2pdg
      integer npid
      integer isib_pid2pdgf2pywrap, isib_pid2pdg
      isib_pid2pdgf2pywrap = isib_pid2pdg(npid)
      end


      subroutine f2pywrapisib_pdg2pid (isib_pdg2pidf2pywrap, npdg)
      external isib_pdg2pid
      integer npdg
      integer isib_pdg2pidf2pywrap, isib_pdg2pid
      isib_pdg2pidf2pywrap = isib_pdg2pid(npdg)
      end


      subroutine f2pywrapgasdev (gasdevf2pywrap, dummy)
      external gasdev
      integer dummy
      double precision gasdevf2pywrap, gasdev
      gasdevf2pywrap = gasdev(dummy)
      end


      subroutine f2pyinits_debug(setupfunc)
      external setupfunc
      integer ncall
      integer ndebug
      integer lun
      common /s_debug/ ncall,ndebug,lun
      call setupfunc(ncall,ndebug,lun)
      end

      subroutine f2pyinits_cldif(setupfunc)
      external setupfunc
      integer ldiff
      common /s_cldif/ ldiff
      call setupfunc(ldiff)
      end

      subroutine f2pyinits_plist(setupfunc)
      external setupfunc
      double precision p(8000,5)
      integer llist(8000)
      integer np
      common /s_plist/ p,llist,np
      call setupfunc(p,llist,np)
      end

      subroutine f2pyinits_cflafr(setupfunc)
      external setupfunc
      double precision par(200)
      integer ipar(100)
      common /s_cflafr/ par,ipar
      call setupfunc(par,ipar)
      end

      subroutine f2pyinits_chist(setupfunc)
      external setupfunc
      integer nnsof(20)
      integer nnjet(20)
      integer jdif(20)
      integer nwd
      integer njet
      integer nsof
      common /s_chist/ nnsof,nnjet,jdif,nwd,njet,nsof
      call setupfunc(nnsof,nnjet,jdif,nwd,njet,nsof)
      end

      subroutine f2pyinitsib_eps(setupfunc)
      external setupfunc
      double precision eps3
      double precision eps5
      double precision eps8
      double precision eps10
      common /sib_eps/ eps3,eps5,eps8,eps10
      call setupfunc(eps3,eps5,eps8,eps10)
      end

      subroutine f2pyinitsib_cst(setupfunc)
      external setupfunc
      double precision pi
      double precision twopi
      double precision cmbarn
      common /sib_cst/ pi,twopi,cmbarn
      call setupfunc(pi,twopi,cmbarn)
      end

      subroutine f2pyinitsib_fac(setupfunc)
      external setupfunc
      double precision facn(8)
      common /sib_fac/ facn
      call setupfunc(facn)
      end

      subroutine f2pyinits_cutoff(setupfunc)
      external setupfunc
      double precision str_mass_val
      double precision str_mass_val_hyp
      double precision str_mass_sea
      common /s_cutoff/ str_mass_val,str_mass_val_hyp,str_mass_sea
      call setupfunc(str_mass_val,str_mass_val_hyp,str_mass_sea)
      end

      subroutine f2pyinits_czdis(setupfunc)
      external setupfunc
      double precision fain
      double precision fb0in
      common /s_czdis/ fain,fb0in
      call setupfunc(fain,fb0in)
      end

      subroutine f2pyinits_czdiss(setupfunc)
      external setupfunc
      double precision fas1
      double precision fas2
      common /s_czdiss/ fas1,fas2
      call setupfunc(fas1,fas2)
      end

      subroutine f2pyinits_czdisc(setupfunc)
      external setupfunc
      double precision zdmax
      double precision epsi
      common /s_czdisc/ zdmax,epsi
      call setupfunc(zdmax,epsi)
      end

      subroutine f2pyinits_czlead(setupfunc)
      external setupfunc
      double precision clead
      double precision flead
      common /s_czlead/ clead,flead
      call setupfunc(clead,flead)
      end

      subroutine f2pyinits_cpspl(setupfunc)
      external setupfunc
      double precision cchik(4,99)
      common /s_cpspl/ cchik
      call setupfunc(cchik)
      end

      subroutine f2pyinits_cnt(setupfunc)
      external setupfunc
      integer itry(20)
      integer nrej(20)
      common /s_cnt/ itry,nrej
      call setupfunc(itry,nrej)
      end

      subroutine f2pyinitckfrag(setupfunc)
      external setupfunc
      integer kodfrag
      common /ckfrag/ kodfrag
      call setupfunc(kodfrag)
      end

      subroutine f2pyinits_run(setupfunc)
      external setupfunc
      double precision sqs
      double precision s
      double precision ptmin
      double precision xmin
      double precision zmin
      integer kb
      integer kt(20)
      integer iat
      common /s_run/ sqs,s,ptmin,xmin,zmin,kb,kt,iat
      call setupfunc(sqs,s,ptmin,xmin,zmin,kb,kt,iat)
      end

      subroutine f2pyinits_parto(setupfunc)
      external setupfunc
      integer nforig(8000)
      integer nporig(8000)
      integer niorig(8000)
      integer ipflag
      integer iiflag
      integer kint
      common /s_parto/ nforig,nporig,niorig,ipflag,iiflag,kint
      call setupfunc(nforig,nporig,niorig,ipflag,iiflag,kint)
      end

      subroutine f2pyinits_plist1(setupfunc)
      external setupfunc
      integer llist1(8000)
      common /s_plist1/ llist1
      call setupfunc(llist1)
      end

      subroutine f2pyinits_chp(setupfunc)
      external setupfunc
      integer ichp(99)
      integer istr(99)
      integer ibar(99)
      common /s_chp/ ichp,istr,ibar
      call setupfunc(ichp,istr,ibar)
      end

      subroutine f2pyinits_spn(setupfunc)
      external setupfunc
      integer iiso(99)
      integer ispn(99)
      common /s_spn/ iiso,ispn
      call setupfunc(iiso,ispn)
      end

      subroutine f2pyinits_chm(setupfunc)
      external setupfunc
      integer ichm(99)
      common /s_chm/ ichm
      call setupfunc(ichm)
      end

      subroutine f2pyinits_cnam(setupfunc)
      external setupfunc
      character namp(100,6)
      common /s_cnam/ namp
      call setupfunc(namp)
      end

      subroutine f2pyinits_rmnt(setupfunc)
      external setupfunc
      double precision xrmass(2)
      double precision xrmex(2)
      integer irmnt(20)
      integer krb
      integer krt(20)
      common /s_rmnt/ xrmass,xrmex,irmnt,krb,krt
      call setupfunc(xrmass,xrmex,irmnt,krb,krt)
      end

      subroutine f2pyinits_pdg2pid(setupfunc)
      external setupfunc
      integer id_pdg_list(99)
      integer id_list(577)
      common /s_pdg2pid/ id_pdg_list,id_list
      call setupfunc(id_pdg_list,id_list)
      end

      subroutine f2pyinits_csydec(setupfunc)
      external setupfunc
      double precision cbr(259)
      integer kdec(1554)
      integer lbarp(99)
      integer idb(99)
      common /s_csydec/ cbr,kdec,lbarp,idb
      call setupfunc(cbr,kdec,lbarp,idb)
      end

      subroutine f2pyinits_kflv(setupfunc)
      external setupfunc
      integer kflv(4,43)
      common /s_kflv/ kflv
      call setupfunc(kflv)
      end

      subroutine f2pyinits_mass1(setupfunc)
      external setupfunc
      double precision am(99)
      double precision am2(99)
      common /s_mass1/ am,am2
      call setupfunc(am,am2)
      end

      subroutine f2pyinits_width1(setupfunc)
      external setupfunc
      double precision aw(99)
      double precision aw2(99)
      common /s_width1/ aw,aw2
      call setupfunc(aw,aw2)
      end

      subroutine f2pyinitnucsig(setupfunc)
      external setupfunc
      double precision sigt
      double precision sigel
      double precision siginel
      double precision sigqe
      double precision sigsd
      double precision sigqsd
      double precision sigppt
      double precision sigppel
      double precision sigppsd
      integer itg
      common /nucsig/ sigt,sigel,siginel,sigqe,sigsd,sigqsd,sigppt
     &,sigppel,sigppsd,itg
      call setupfunc(sigt,sigel,siginel,sigqe,sigsd,sigqsd,sigppt,
     &sigppel,sigppsd,itg)
      end

      subroutine f2pyinitsib_rnk(setupfunc)
      external setupfunc
      integer lrnk(8000)
      common /sib_rnk/ lrnk
      call setupfunc(lrnk)
      end

      subroutine f2pyinits_ccsig(setupfunc)
      external setupfunc
      double precision ssig(61,3)
      double precision pjetc(21,81,61,2)
      double precision ssign(61,3)
      double precision ssignsd(61,3)
      double precision alint(61,3)
      double precision asqsmin
      double precision asqsmax
      double precision dasqs
      integer nsqs
      common /s_ccsig/ ssig,pjetc,ssign,ssignsd,alint,asqsmin,asqs
     &max,dasqs,nsqs
      call setupfunc(ssig,pjetc,ssign,ssignsd,alint,asqsmin,asqsma
     &x,dasqs,nsqs)
      end

      subroutine f2pyinits_ccsig2(setupfunc)
      external setupfunc
      double precision ssig_tot(61,3)
      double precision ssig_sd1(61,3)
      double precision ssig_sd2(61,3)
      double precision ssig_dd(61,3)
      double precision ssig_b(61,3)
      double precision ssig_rho(61,3)
      common /s_ccsig2/ ssig_tot,ssig_sd1,ssig_sd2,ssig_dd,ssig_b,
     &ssig_rho
      call setupfunc(ssig_tot,ssig_sd1,ssig_sd2,ssig_dd,ssig_b,ssi
     &g_rho)
      end

      subroutine f2pyinits_czgen(setupfunc)
      external setupfunc
      double precision xa(2)
      double precision xb(2)
      double precision xmax
      double precision za(2)
      double precision zb(2)
      double precision zmax
      double precision dx(2)
      double precision dz(2)
      double precision apart(2)
      double precision ffa(2)
      double precision ffb(2)
      double precision dfx(2)
      double precision dfz(2)
      double precision xx(200,2)
      double precision zz(200,2)
      double precision ffx(200,2)
      double precision ffz(200,2)
      integer nx
      integer nz
      common /s_czgen/ xa,xb,xmax,za,zb,zmax,dx,dz,apart,ffa,ffb,d
     &fx,dfz,xx,zz,ffx,ffz,nx,nz
      call setupfunc(xa,xb,xmax,za,zb,zmax,dx,dz,apart,ffa,ffb,dfx
     &,dfz,xx,zz,ffx,ffz,nx,nz)
      end

      subroutine f2pyinitfragmod(setupfunc)
      external setupfunc
      double precision a(10,10,20)
      double precision ae(10,10,20)
      double precision eres(10,10)
      integer nflagg(10,10)
      common /fragmod/ a,ae,eres,nflagg
      call setupfunc(a,ae,eres,nflagg)
      end

      subroutine f2pyinitcnucms(setupfunc)
      external setupfunc
      double precision b
      double precision bmax
      integer ntry
      integer na
      integer nb
      integer ni
      integer nael
      integer nbel
      integer jja(56)
      integer jjb(56)
      integer jjint(56,56)
      integer jjael(56)
      integer jjbel(56)
      common /cnucms/ b,bmax,ntry,na,nb,ni,nael,nbel,jja,jjb,jjint
     &,jjael,jjbel
      call setupfunc(b,bmax,ntry,na,nb,ni,nael,nbel,jja,jjb,jjint,
     &jjael,jjbel)
      end

      subroutine f2pyinithepevt(setupfunc)
      external setupfunc
      integer nevhep
      integer nhep
      integer isthep(8000)
      integer idhep(8000)
      integer jmohep(2,8000)
      integer jdahep(2,8000)
      double precision phep(5,8000)
      double precision vhep(4,8000)
      common /hepevt/ nevhep,nhep,isthep,idhep,jmohep,jdahep,phep,
     &vhep
      call setupfunc(nevhep,nhep,isthep,idhep,jmohep,jdahep,phep,v
     &hep)
      end

      subroutine f2pyinitschg(setupfunc)
      external setupfunc
      integer ichg(8000)
      common /schg/ ichg
      call setupfunc(ichg)
      end

      subroutine f2pyinitnpy(setupfunc)
      external setupfunc
      integer*8 bitgen
      common /npy/ bitgen
      call setupfunc(bitgen)
      end


