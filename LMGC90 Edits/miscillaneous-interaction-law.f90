
!!! in mod_DKDKx.f90, end of subroutine compute_contact_DKDKx. 
do icdan=1,nb_DKDKx
      adjac(this(icdan)%icdtac)%icdan(this(icdan)%iadj) = icdan   

      if (tact_behav(this(icdan)%lawnb)%ilaw == i_MAGNETIC_MP_REPELL .OR. tact_behav(this(icdan)%lawnb)%ilaw == i_MAGNETIC_MP_ATTRACT) then 
         this(icdan)%internal(1) = nonuc
      end if
   end do
   

!!! in mod_tact_behav.f90, in subroutine read_xxx_tact_behav

   case('MAGNETIC_MP_REPELL            ')

            nb_param = 2 ! mag charge and friction on contact? 

            allocate(param(nb_param))

            iparam = 1
            call read_single(behav,param,iparam) ! fric
            
            if( .not. read_G_clin()) goto 10
            iparam = 2
            call read_single(behav,param,iparam) ! mag charge
            
               !123456789012345678901234567890
          case('MAGNETIC_MP_ATTRACT           ')

            nb_param = 2 ! mag charge and friction on contact? 

            allocate(param(nb_param))

            iparam = 1
            call read_single(behav,param,iparam) ! fric
            
            if( .not. read_G_clin()) goto 10
            iparam = 2
            call read_single(behav,param,iparam) ! mag charge
            
!!! in subroutine write_xxx_tact_behav

        case(i_MAGNETIC_MP_REPELL, i_MAGNETIC_MP_ATTRACT)
          call write_single(clin ,1,tact_behav(ibehav)%param,tact_behav(ibehav)%param_name,nfich)
          call write_single(clin0,2,tact_behav(ibehav)%param,tact_behav(ibehav)%param_name,nfich)

        
!!! new subroutine in mod_tact_behav.f90

subroutine get_Qm(ibehav,Qm) bind(C, name="get_qm_")
   implicit none
   !> contact law id
   integer(kind=4), intent(in) :: ibehav
   !> g0 parameter of the law
   real(kind=8), intent(out) :: Qm
   !
   character(len=14) :: IAM
   character(len=80) :: cout
   !      12345678901234
   IAM = 'tact_behav::Qm'

   Qm = 0.d0

   select case(tact_behav(ibehav)%ilaw)
   case(i_MAGNETIC_MP_REPELL, &
        i_MAGNETIC_MP_ATTRACT, &
        i_MAGNETIC_DIPOLE)

     Qm = tact_behav(ibehav)%param(2)

   case default
     write(cout,'(A,A,A)')' lawty ',tact_behav(ibehav)%lawty,' not implemented'
     call faterr(IAM,cout)
   end select

 end subroutine 
 

!!! in subroutine tact_behav_info_by_id

  case(i_MAGNETIC_MP_REPELL)
      nb_param = 2
      allocate(param_name(nb_param))
      param_name(1) = 'fric'
      param_name(2) = 'Qm'

      nb_internal = 1
      !                         12345678901234
      internal_comment(2:15) = 'gapREF        '
    
    case(i_MAGNETIC_MP_ATTRACT)
      nb_param = 2
      allocate(param_name(nb_param))
      param_name(1) = 'fric'
      param_name(2) = 'Qm'

      nb_internal = 1
      !                         12345678901234
      internal_comment(2:15) = 'gapREF        '

